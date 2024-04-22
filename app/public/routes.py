import logging
import app

from flask import request, current_app, render_template

from . import public_bp
from ..dataset.models import DataSet, DSMetaData, DSDownloadRecord, DSViewRecord, FileDownloadRecord, FileViewRecord, Rating, FeatureModel
from sqlalchemy import func
from app import db

logger = logging.getLogger(__name__)


@public_bp.route("/")
def index():
    logger.info('Access index')

    latest_datasets = DataSet.query.join(DSMetaData).filter(
        DSMetaData.dataset_doi.isnot(None)
    ).order_by(DataSet.created_at.desc()).limit(5).all()

    datasets_counter = app.datasets_counter()
    feature_models_counter = app.feature_models_counter()

     # Downloads
    total_dataset_downloads = DSDownloadRecord.query.count()
    total_feature_model_downloads = FileDownloadRecord.query.count()

    # Views
    total_dataset_views = DSViewRecord.query.count()
    total_feature_model_views = FileViewRecord.query.count()

    # Ratings
    total_dataset_ratings = Rating.query.filter(Rating.dataset_id != None).count()
    total_feature_model_ratings = Rating.query.filter(Rating.feature_model_id != None).count()

    return render_template("public/index.html",
                           datasets=latest_datasets,
                           datasets_counter=datasets_counter,
                           feature_models_counter=feature_models_counter,
                           total_dataset_downloads=total_dataset_downloads,
                           total_feature_model_downloads=total_feature_model_downloads,
                           total_dataset_views=total_dataset_views,
                           total_feature_model_views=total_feature_model_views,
                           total_dataset_ratings=total_dataset_ratings,
                           total_feature_model_ratings=total_feature_model_ratings)
