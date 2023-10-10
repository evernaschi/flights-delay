from typing import Tuple, Union, List
import pickle
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from .utils import (
    get_period_day,
    is_high_season,
    get_min_diff,
    FEATURES_COLS,
    THRESHOLD_IN_MINUTES,
)

FILE_NAME = "model.pkl"


class DelayModel:
    def __init__(self):
        self._model = None  # Model should be saved in this attribute.

    def preprocess(
        self, data: pd.DataFrame, target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        if not target_column:
            features = pd.get_dummies(data, columns=["OPERA", "TIPOVUELO", "MES"])
            features = features.reindex(columns=FEATURES_COLS, fill_value=0)
            return features

        data["period_day"] = data["Fecha-I"].apply(get_period_day)
        data["high_season"] = data["Fecha-I"].apply(is_high_season)
        data["min_diff"] = data.apply(get_min_diff, axis=1)
        data["delay"] = np.where(data["min_diff"] > THRESHOLD_IN_MINUTES, 1, 0)

        features = pd.concat(
            [
                pd.get_dummies(data["OPERA"], prefix="OPERA"),
                pd.get_dummies(data["TIPOVUELO"], prefix="TIPOVUELO"),
                pd.get_dummies(data["MES"], prefix="MES"),
            ],
            axis=1,
        )
        features = features[FEATURES_COLS]
        target = data[[target_column]]
        return (features, target)

    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """

        y_train = target.squeeze()  # Data Series needed here instead of DataFrame
        n_y0 = len(target[y_train == 0])
        n_y1 = len(target[y_train == 1])

        self._model = LogisticRegression(
            class_weight={1: n_y0 / len(y_train), 0: n_y1 / len(y_train)}
        )
        self._model.fit(features, target)

    def predict(self, features: pd.DataFrame) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.

        Returns:
            (List[int]): predicted targets.
        """
        if not self._model:
            raise ValueError("The model has not been fitted.")
        predictions = self._model.predict(features).tolist()
        return predictions


def create_model():
    model = DelayModel()
    data = pd.read_csv(filepath_or_buffer="./data/data.csv")
    features, target = model.preprocess(data=data, target_column="delay")
    model.fit(features=features, target=target)
    with open(FILE_NAME, "wb") as file:
        pickle.dump(model, file)


def load_model():
    try:
        with open(FILE_NAME, "rb") as file:
            model = pickle.load(file)
            if model:
                return model
            raise ValueError("Invalid or unsupported model format.")
    except FileNotFoundError as exc:
        raise FileNotFoundError("Model file not found.") from exc


def get_model():
    try:
        model = load_model()
        return model
    except FileNotFoundError:
        create_model()
        model = load_model()
        return model
