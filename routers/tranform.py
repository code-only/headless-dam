# routers/transform.py
from uuid import UUID
import tempfile
import os
from fastapi import APIRouter, Path, Query, HTTPException, Response


from utils.s3_utils import download_file_from_s3
from utils.image_transform import transform_image
from utils.pdf_transform import pdf_to_image
from utils.video_transform import video_to_thumbnail

router = APIRouter()

S3_BUCKET = "your-bucket"


def get_asset_s3_key(asset_id: UUID) -> str:
    """
    Get the S3 key for an asset based on its ID.
    This is a placeholder function that should be implemented to retrieve the
    actual S3 key from a database or other storage.
    """
    # TODO: Implement logic to get S3 key from asset_id (e.g., DB lookup)
    return f"assets/{asset_id}"


@router.get("/image/{id}")
async def transform_image_endpoint(
    id: UUID = Path(..., description="Asset ID"),
    width: int = Query(None, gt=0, le=4096),
    height: int = Query(None, gt=0, le=4096),
    crop: bool = Query(False),
    format: str = Query(None, regex="^(jpg|jpeg|png|webp|gif|tiff|bmp)$"),
    quality: int = Query(80, ge=1, le=100),
):
    """
    Transform an image asset by resizing, cropping, and changing format.
    """
    s3_key = get_asset_s3_key(id)
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input")
        output_path = os.path.join(tmpdir, "output")
        if not download_file_from_s3(S3_BUCKET, s3_key, input_path):
            raise HTTPException(404, "Asset not found in S3")
        try:
            transform_image(
                input_path, output_path, width, height, crop, format, quality
            )
            with open(output_path, "rb") as f:
                return Response(
                    content=f.read(), media_type=f"image/" + (format or "jpeg")
                )
        except Exception as e:
            raise HTTPException(500, f"Image transformation failed: {e}")


@router.get("/pdf/{id}")
async def transform_pdf_endpoint(
    id: UUID = Path(..., description="Asset ID"),
    page: int = Query(1, ge=1, description="PDF page number to render"),
    dpi: int = Query(200, ge=72, le=600, description="DPI for rendering"),
):
    """
    Transform a PDF asset by rendering a specific page as an image.
    """
    s3_key = get_asset_s3_key(id)
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.pdf")
        output_path = os.path.join(tmpdir, "output.jpg")
        if not download_file_from_s3(S3_BUCKET, s3_key, input_path):
            raise HTTPException(404, "Asset not found in S3")
        try:
            pdf_to_image(input_path, output_path, page=page, dpi=dpi)
            with open(output_path, "rb") as f:
                return Response(content=f.read(), media_type="image/jpeg")
        except Exception as e:
            raise HTTPException(500, f"PDF transformation failed: {e}")


@router.get("/video/{id}")
async def transform_video_endpoint(
    id: UUID = Path(..., description="Asset ID"),
    time: float = Query(1.0, ge=0, description="Timestamp (in seconds) for thumbnail"),
):
    """
    Transform a video asset by extracting a thumbnail at a specific time.
    """
    s3_key = get_asset_s3_key(id)
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.mp4")
        output_path = os.path.join(tmpdir, "output.jpg")
        if not download_file_from_s3(S3_BUCKET, s3_key, input_path):
            raise HTTPException(404, "Asset not found in S3")
        try:
            video_to_thumbnail(input_path, output_path, time=time)
            with open(output_path, "rb") as f:
                return Response(content=f.read(), media_type="image/jpeg")
        except Exception as e:
            raise HTTPException(500, f"Video transformation failed: {e}")


@router.get("/default/{id}")
async def transform_default_endpoint(
    id: UUID = Path(..., description="Asset ID"),
):
    """
    Fallback endpoint for unsupported file types.
    """
    # Optionally, return a generic icon, error, or the original file.
    raise HTTPException(415, "Transformation not supported for this file type.")

