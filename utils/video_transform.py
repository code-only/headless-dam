# utils/video_transform.py
import ffmpeg


def video_to_thumbnail(input_path: str, output_path: str, time: float = 1.0):
    """
    Extract a thumbnail from a video at a specific timestamp.
    :param input_path: Path to the input video file.
    :param output_path: Path to save the thumbnail image.
    :param time: Timestamp in seconds to extract the thumbnail (default is 1.0).
    """
    (
        ffmpeg.input(input_path, ss=time)
        .output(output_path, vframes=1)
        .run(overwrite_output=True)
    )

