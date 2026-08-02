from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score)

def build_ml_dataset(df):
    columns = ["returns","momentum", "volatility", "trend_strength","volume_ratio","target"]
    return df[columns].dropna()

def train_test_split_ml(df, train_ratio=0.7):
    split_idx = int(len(df) * train_ratio)

    train = df.iloc[:split_idx].copy()
    test = df.iloc[split_idx:].copy()

    return train, test

def train_logistic(train_df):

    feature_columns = [
        "momentum",
        "volatility",
        "trend_strength",
        "volume_ratio"
    ]

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

def train_randforest(train_df):

    feature_columns = [
        "momentum",
        "volatility",
        "trend_strength",
        "volume_ratio"
    ]

    train_df = train_df.dropna(
        subset=feature_columns + ["target"]
    )

    X = train_df[feature_columns]
    y = train_df["target"]

    model = RandomForestClassifier()

    model.fit(X, y)

    predictions = model.predict(X)

    metrics = {
        "Accuracy": accuracy_score(y, predictions),
        "Precision": precision_score(y, predictions),
        "Recall": recall_score(y, predictions)
    }

    return model, metrics



def evaluate_model(model, test_df):

    feature_columns = [
        "momentum",
        "volatility",
        "trend_strength",
        "volume_ratio"
    ]

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