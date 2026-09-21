from sklearn.ensemble import IsolationForest


def detect_anomalies(
    amounts: list[float],
    contamination: float = 0.1,
) -> list[dict]:
    """Detect unusual transaction amounts using Isolation Forest."""

    if len(amounts) < 2:
        raise ValueError("At least two transactions are required.")

    model = IsolationForest(
        contamination=contamination,
        random_state=42,
    )

    features = [[amount] for amount in amounts]

    predictions = model.fit_predict(features)
    scores = model.decision_function(features)

    results = []

    for amount, prediction, score in zip(
        amounts,
        predictions,
        scores,
    ):
        results.append(
            {
                "amount": amount,
                "is_anomaly": prediction == -1,
                "anomaly_score": round(float(score), 4),
            }
        )

    return results