import numpy as np


def get_i0(rgb_im, mask_im):
    # Get I0 for individual channels
    if rgb_im.shape[-1] > 3:
        rgb_im = rgb_im[..., :3]
    rbg_im = rgb_im.astype(float)

    ch_i0 = []
    for ch in range(rbg_im.shape[2]):
        ch_i0.append(np.median(rbg_im[..., ch][mask_im < 1]))
    return ch_i0


def get_od(rgb_im, ch_i0):
    # convert image to optical density (aka staining darkness (SDA)) image
    if rgb_im.shape[-1] > 3:
        rgb_im = rgb_im[..., :3]
    rgb_im = rgb_im.astype(float)
    od_im = np.zeros_like(rgb_im)
    for ch in range(od_im.shape[2]):
        rgb_im[..., ch][rgb_im[..., ch] > ch_i0[ch]] = ch_i0[ch]
        od_im[..., ch] = -np.log10(rgb_im[..., ch] / ch_i0[ch])
    return od_im


def mask_od(od_im, mask_im, bg_threshold=0.01):
    od_mask = od_im > bg_threshold

    # mask out other unwanted regions using mask file
    for ch in range(od_im.shape[2]):
        od_im[..., ch] = od_im[..., ch] * (mask_im > 0)

    # apply the mask to the optical density image
    od_im = od_im * (od_mask > 0)

    # remove infinities and nans
    od_im[od_im == np.Inf] = 0
    od_im[np.isnan(od_im)] = 0
    return od_im, od_mask


def flatten_and_threshold(od_im, beta=0.15):
    # flatten image but keep 3 channels separate
    od_flat = od_im.reshape((-1, od_im.shape[-1])).T

    # only keep values above the higher optical density threshold
    od_thresholded = od_flat[:, (od_flat > beta).any(axis=0)]
    return od_thresholded


def od_pca(od_thresholded):
    # center the values for sv decomposition
    centered = (od_thresholded.T - np.mean(od_thresholded, axis=1)).T

    # get principal components using svd
    pcs = np.linalg.svd(centered.astype(float), full_matrices=False)[0].astype(centered.dtype)
    return pcs


def project_od(od_thresholded, pcs):
    # project data on the top 2 components
    projection = pcs.T[:-1].dot(od_thresholded)

    # normalize projection
    magnitude = np.sqrt((projection ** 2).sum(0))
    normalized_projection = projection / magnitude
    return normalized_projection


def get_angles(normalized_projection, alpha=0.01):
    # get projection angles towards x w.r.t. y of normalized projection
    low_angle_perc = alpha
    high_angle_perc = 1 - alpha
    angles = (1 - normalized_projection[1]) * np.sign(normalized_projection[0])

    # get index where angle is the low percentile
    low_idx = int(low_angle_perc * angles.size + 0.5)
    angle_low_idx = np.argpartition(angles, low_idx)[low_idx]

    # get index where angle is the high percentile
    high_idx = int(high_angle_perc * angles.size + 0.5)
    angle_high_idx = np.argpartition(angles, high_idx)[high_idx]
    return angle_low_idx, angle_high_idx


def calculate_stain_matrix(pcs, normalized_projection, angle_low_idx, angle_high_idx):
    # convert values to od space
    min_v = pcs[:, :-1].dot(normalized_projection[:, angle_low_idx])
    max_v = pcs[:, :-1].dot(normalized_projection[:, angle_high_idx])
    v_matrix = np.array([min_v, max_v]).T
    normalized_v = v_matrix / np.sqrt((v_matrix ** 2).sum(0))

    # construct stain matrix
    stain_0 = normalized_v[:, 0]
    stain_1 = normalized_v[:, 1]
    stain_2 = np.cross(stain_0, stain_1)

    # ensures more blue layer is stain_1 to get correct order for output
    if stain_0[0] > stain_1[0]:
        stain_0, stain_1 = stain_1, stain_0

    # normalize stain matrix
    stains = np.array([stain_0, stain_1, stain_2 / np.linalg.norm(stain_2)]).T
    stains_norm = stains / np.sqrt((stains ** 2).sum(0))
    return stains_norm


def get_stain_matrix(od_im, alpha=0.01, beta=0.15):
    od_thresholded = flatten_and_threshold(od_im, beta)
    pcs = od_pca(od_thresholded)
    normalized_projection = project_od(od_thresholded, pcs)
    angle_low_idx, angle_high_idx = get_angles(normalized_projection, alpha)
    stains_norm = calculate_stain_matrix(pcs, normalized_projection, angle_low_idx, angle_high_idx)
    return stains_norm


def deconvolve_od(od_im, stains_norm):
    od_flat = od_im.reshape((-1, od_im.shape[-1])).T
    stains_inv = np.linalg.pinv(stains_norm)
    deconv_od_matrix = np.dot(stains_inv, od_flat)
    return deconv_od_matrix


def get_od_decon_im(od_im, deconv_od_matrix):
    # convertOD matrix back to 3D image for visualization and quantification
    deconv_od_im = deconv_od_matrix.T.reshape(od_im.shape[:-1] + (deconv_od_matrix.shape[0],))
    return deconv_od_im


def get_rgb_decon_im(rgb_im, deconv_od_matrix, ch_i0):
    # convert od to rgb matrix for visualization
    deconv_rgb_matrix_float = np.zeros_like(deconv_od_matrix)
    for ch in range(deconv_rgb_matrix_float.shape[0]):
        deconv_rgb_matrix_float[ch, :] = ch_i0[ch] * 10 ** (-deconv_od_matrix[ch, :])
    deconv_rgb_int = deconv_rgb_matrix_float.clip(0, 255)

    # convert RGB matrix back to 3D image for visualization
    deconv_rgb_im = deconv_rgb_int.T.reshape(rgb_im.shape[:-1] + (deconv_rgb_int.shape[0],))
    return deconv_rgb_im


def run_full(rgb_im, mask_im):
    ch_i0 = get_i0(rgb_im, mask_im)
    od_im, _ = mask_od(get_od(rgb_im, ch_i0), mask_im)
    stains_norm = get_stain_matrix(od_im)
    deconv_od_matrix = deconvolve_od(od_im, stains_norm)
    deconv_od_im = get_od_decon_im(od_im, deconv_od_matrix)
    deconv_rgb_im = get_rgb_decon_im(rgb_im, deconv_od_matrix, ch_i0)
    return deconv_od_im, deconv_rgb_im, stains_norm

