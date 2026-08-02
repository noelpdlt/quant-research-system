from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score)


def feature_version(version):
    if version == 'v1':
        feature_columns = [
            "momentum",
            "volatility",
            "trend_strength",
            "volume_ratio"
        ]
    if version == 'v2':
        feature_columns = [
                "momentum",
                "volatility",
                "trend_strength",
                "volume_ratio",
                "ma5",
                "rsi",
                "distance_ma20"
            ]
    return feature_columns

def build_ml_dataset(df, feature_columns):
    columns = feature_columns + ["returns", "target"]
    return df[columns].dropna()

def train_test_split_ml(df, train_ratio=0.7):
    split_idx = int(len(df) * train_ratio)

    train = df.iloc[:split_idx].copy()
    test = df.iloc[split_idx:].copy()

    return train, test

def train_logistic(train_df, feature_set = "v1"):
    feature_columns = feature_version(feature_set)
    train_df = train_df.dropna(
        subset=feature_columns + ["target"]
    )

    X = train_df[feature_columns]
    y = train_df["target"]

    model = LogisticRegression()

    model.fit(X, y)

    predictions = model.predict(X)

    metrics = {
        "Accuracy": accuracy_score(y, predictions),
        "Precision": precision_score(y, predictions),
        "Recall": recall_score(y, predictions)
    }

    return model, metrics

def train_randforest(train_df, feature_set = 'v1', random_state=123):
    feature_columns = feature_version(feature_set)
    train_df = train_df.dropna(
        subset=feature_columns + ["target"]
    )

    X = train_df[feature_columns]
    y = train_df["target"]

    model = RandomForestClassifier(
        random_state=random_state
    )

    model.fit(X, y)

    predictions = model.predict(X)

    metrics = {
        "Accuracy": accuracy_score(y, predictions),
        "Precision": precision_score(y, predictions),
        "Recall": recall_score(y, predictions)
    }

    return model, metrics

def evaluate_model(model, test_df, feature_set='v1'):

    feature_columns = feature_version(feature_set)

    X = test_df[feature_columns]
    y = test_df["target"]

    prediction = model.predict(X)

    print(
        f"Accuracy: {accuracy_score(y,prediction):.3f}"
    )
    print(
        f"Precision: {precision_score(y,prediction):.3f}"
    )
    print(
        f"Recall: {recall_score(y,prediction):.3f}"
    )