import cv2
import numpy as np
from PIL import ImageGrab

_DEFAULT_CONFIDENCE = 0.99

def locateOnImage(image: cv2.Mat, template: cv2.Mat, confidence: float = _DEFAULT_CONFIDENCE, debug: bool = False) -> list[tuple[int, int]]:
    """Locates occurences of a template on an image.

    Args:
        image (cv2.Mat): Image we will search on.
        template (cv2.Mat): Template to search on the image.
        confidence (float, optional): Confidence in the similarity. Defaults to 0.99.
        debug (bool, optional) View the result in a new window. Default to False.

    Returns:
        list[tuple[int, int]]: List of coordinates stored in a tuple
    """
    results: list[tuple[int, int]] = []

    # RGB to BGR
    hh, ww = template.shape[:2]
    base = template[:, :, 0:3]
    try:
        alpha = template[:, :, 3]
        alpha = cv2.merge([alpha, alpha, alpha])

        # do masked template matching and save correlation image
        correlation = cv2.matchTemplate(
            image, base, cv2.TM_CCORR_NORMED, mask=alpha)
    except IndexError:
        correlation = cv2.matchTemplate(image, base, cv2.TM_CCORR_NORMED)
    locations = np.where(correlation >= confidence)  # type: ignore

    # Iterate through matches
    if debug:
        result = image.copy()
    for match in zip(*locations[::-1]):
        results.append((match[0]+ww/2, match[1]+hh/2))  # type: ignore
        if debug:
            cv2.rectangle(result, match, (match[0]+ww, match[1]+hh), (0, 0, 255), 1)
    if debug:
        cv2.imshow('result', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return results


def locateOnScreen(template: cv2.Mat, confidence: float = _DEFAULT_CONFIDENCE, debug: bool = False) -> list[tuple[int, int]]:
    """Locates occurences of a template on screen.

    Args:
        template (cv2.Mat): Template to match on the screen.
        confidence (float, optional): Confidence in the similarity. Defaults to 0.99.
        debug (bool, optional) View the result in a new window. Default to False.

    Returns:
        list[tuple[int, int]]: List of coordinates stored in a tuple
    """
    # Convert PIL to RGB np array
    screenshot = np.array(ImageGrab.grab().convert('RGB'))
    screenshot = screenshot[:, :, ::-1]  # Convert RGB to BGR

    return locateOnImage(screenshot, template, confidence, debug)


def locateAllOnImage(image: cv2.Mat, templates: list[cv2.Mat], confidences: list[float] = [], debug: bool = False) -> list[tuple[int, int]]:
    """Locates occurences of a template on an image.

    Args:
        image (cv2.Mat): Image we will search on.
        templates (list[cv2.Mat]): Template to search on the image.
        confidence (list[float], optional): Confidences in the similarity. Defaults to 0.99.
        debug (bool, optional) View the result in a new window. Default to False.

    Returns:
        list[tuple[int, int]]: List of coordinates stored in a tuple
    """
    if len(confidences) < len(templates):
        confidences = [_DEFAULT_CONFIDENCE]*(len(templates)-len(confidences))
    results: list[tuple[int, int]] = []

    result = image.copy()
    for i in range(len(templates)):
        # RGB to BGR
        hh, ww = templates[i].shape[:2]
        base = templates[i][:, :, 0:3]
        try:
            alpha = templates[i][:, :, 3]
            alpha = cv2.merge([alpha, alpha, alpha])

            # do masked template matching and save correlation image
            correlation = cv2.matchTemplate(
                image, base, cv2.TM_CCORR_NORMED, mask=alpha)
        except IndexError:
            correlation = cv2.matchTemplate(image, base, cv2.TM_CCORR_NORMED)
        locations = np.where(correlation >= confidences[i])  # type: ignore

        # Iterate through matches
        for match in zip(*locations[::-1]):
            results.append((match[0]+ww/2, match[1]+hh/2))  # type: ignore
            if debug:
                cv2.rectangle(result, match, (match[0]+ww, match[1]+hh), (0, 0, 255), 1)
    if debug:
        print(f"Found {len(results)} matches")
        cv2.imshow('result', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return results


def locateAllOnScreen(templates: list[cv2.Mat], confidences: list[float] = [], debug: bool = False) -> list[tuple[int, int]]:
    """Locates occurences of a template on screen.

    Args:
        templates (list[cv2.Mat]): Templates to match on the screen.
        confidences (list[float], optional): Confidences in the similarity. Defaults to 0.99.
        debug (bool, optional) View the result in a new window. Default to False.

    Returns:
        list[tuple[int, int]]: List of coordinates stored in a tuple
    """
    # Convert PIL to RGB np array
    screenshot = np.array(ImageGrab.grab().convert('RGB'))
    screenshot = screenshot[:, :, ::-1]  # Convert RGB to BGR

    return locateAllOnImage(screenshot, templates, confidences, debug)
