def resize(orig, limitation, upscale=False):
    """
    Restrict image size in a given box. Return resized resolution.

    - limitation
        e.g.: (1920, 1080), (1920, -1)

    Arguments:
        orig: (w, h)
        limitation: (w, h)

    Keyword Arguments:
        upscale: Bool
            True: upscale if orig < limitation
            False: not upscale [default]

    Returns:
        (w, h)
    """

    Orig_w = orig[0]
    Orig_h = orig[1]
    Lmt_w = limitation[0]
    Lmt_h = limitation[1]

    if Lmt_w <= 0:
        if upscale is False:
            if Orig_h <= Lmt_h:
                return (Orig_w, Orig_h)
            else:
                return (Lmt_h * Orig_w / Orig_h, Lmt_h)  # (Orig_w / (Orig_h / Lmt_h), Lmt_h)
        else:
            return (Lmt_h * Orig_w / Orig_h, Lmt_h)
    elif Lmt_h <= 0:
        if upscale is False:
            if Orig_w <= Lmt_w:
                return (Orig_w, Orig_h)
            else:
                return (Lmt_w, Lmt_w * Orig_h / Orig_w)  # (Lmt_w, Orig_h / (Orig_w / Lmt_w))
        else:
            return (Lmt_w, Lmt_w * Orig_h / Orig_w)

    elif Orig_h * Lmt_w > Lmt_h * Orig_w:  # (Orig_h / Orig_w) > (Lmt_h / Lmt_w)
        if upscale is False:
            if Orig_h <= Lmt_h:
                return (Orig_w, Orig_h)
            else:
                return (Lmt_h * Orig_w / Orig_h, Lmt_h)
        else:
            return (Lmt_h * Orig_w / Orig_h, Lmt_h)
    else:
        if upscale is False:
            if Orig_w <= Lmt_w:
                return (Orig_w, Orig_h)
            else:
                return (Lmt_w, Lmt_w * Orig_h / Orig_w)
        else:
            return (Lmt_w, Lmt_w * Orig_h / Orig_w)
