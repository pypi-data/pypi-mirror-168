import numpy as np


def _guess_dynamic_range(image, default=-1):
    """Try to guess the maximum pixel value for the image.

    If not possible, the default value is returned.  An exception is
    raised if the default is -1.
    """
    if image.dtype == np.uint8:
        return 255
    elif image.dtype == np.uint16:
        return 65535
    elif np.issubdtype(image.dtype, np.floating) and image.max() <= 1 and image.min() >= 0:
        return 1
    if default == -1:
        raise ValueError("Cannot guess the dynamic range")
    return default


def mse(image1, image2, dtype=np.float32):
    """Mean Squared Error (MSE).

    Note: independently on the dynamic range of the input, the metric
    is scaled as if values were in the [0, 1] range.

    """
    dr = max(_guess_dynamic_range(image1), _guess_dynamic_range(image2))
    diff = np.subtract(image1, image2, dtype=dtype)
    val = (diff ** 2).mean(dtype=dtype)
    return val / (dr * dr)


def psnr(image1, image2, dtype=np.float32):
    """Peak Signal to Noise Ratio (PSNR)."""
    mse_val = mse(image1, image2, dtype)
    if mse_val > 0:
        return -10 * np.log10(mse_val)
    else:
        return np.inf


def _ssim_window(image, window=8):
    """Extract the windows for SSIM computation."""
    if image.ndim != 3:
        image = image.reshape(image.shape[0], image.shape[1], -1)
    h, w, c = image.shape
    hb = h // window
    wb = w // window
    if h % window != 0 or w % window != 0:
        # Make sure that the image dimensions are multiples of the window
        image = image[:hb * window, :wb * window, :]
    windows = image.reshape(hb, window, wb, window, -1)
    windows = windows.transpose(0, 2, 4, 1, 3)
    return windows.reshape(-1, window * window)


def ssim(image1, image2, window=8, dynamic_range=None, dtype=np.float32):
    """Structural Simularity Index Measure (SSIM).

    Args:
        image1 (array): first image
        image2 (array): second image
        window (int): size of the local window
        dynamic_range (float): maximum value in the image
        dtype (dtype): type for internal computations

    Returns:
        (float) the SSIM between the two images.

    Input images can have two (grayscale) or more (color)
    dimensions. Their size must match exactly.  If not given the
    dynamic range is 255 for eight-bit images and 1 for floating point
    images (if all values are in the [0, 1] range).

    """
    k1 = 0.01
    k2 = 0.03
    if dynamic_range is None:
        if image1.dtype == np.uint8 and image2.dtype == np.uint8:
            dynamic_range = 255
        elif all(np.issubdtype(im.dtype, np.floating) for im in (image1, image2)):
            if image1.max() > 1 or image1.min() > 1 or image1.min() < 0 or image2.min() < 0:
                raise ValueError("SSIM: Cannot guess the dynamic range")
            dynamic_range = 1
        else:
            raise ValueError("SSIM: Cannot guess the dynamic range")
    c1 = (k1 * dynamic_range) ** 2
    c2 = (k2 * dynamic_range) ** 2
    win1 = _ssim_window(image1)
    win2 = _ssim_window(image2)
    mu1 = win1.mean(1, dtype=dtype)
    mu2 = win2.mean(1, dtype=dtype)
    sigma1 = win1.var(1, dtype=dtype)
    sigma2 = win2.var(1, dtype=dtype)
    cov = np.multiply(win1, win2, dtype=dtype).mean(1, dtype=dtype) - mu1 * mu2
    num = (2 * mu1 * mu2 + c1) * (2 * cov + c2)
    den = (mu1 ** 2 + mu2 ** 2 + c1) * (sigma1 + sigma2 + c2)
    return (num / den).mean(dtype=dtype)


def _test():
    image1 = (np.arange(1800) % 256).reshape(30, 20, 3).astype(np.uint8)
    image2 = image1[::-1, :, :]
    print(mse(image1, image2))
    print(psnr(image1, image2))
    print(ssim(image1, image2))


if __name__ == "__main__":
    _test()
