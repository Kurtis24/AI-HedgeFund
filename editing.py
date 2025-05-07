import argparse
import requests
import datetime


def get_technical_signal(api_key: str) -> dict:
    """
    Fetches the technical analysis score from an API.

    Returns a dict with:
      - symbol (str)
      - tech_score (float)   # technical signal score in [0,1]
      - price (float)
      - stop_pct (float)     # stop-loss as fraction
      - buy_time (datetime)
    """
    url = "https://api.techbot.example.com/recommend"  # Replace with actual endpoint
    resp = requests.get(url, params={"api_key": api_key})
    resp.raise_for_status()
    data = resp.json()

    return {
        "symbol": data["symbol"],
        "tech_score": float(data.get("tech_score", data.get("score", 0.0))),
        "price": float(data["price"]),
        "stop_pct": float(data["stop_loss_pct"]),
        "buy_time": datetime.datetime.fromisoformat(data["buy_time"])
    }


def decide_position(tech_score: float, sent_score: float) -> float:
    """
    Combine technical and sentiment scores by simple addition.

    Returns:
        float: combined score (can range from 0 to 2).
    """
    if not (0 <= tech_score <= 1 and 0 <= sent_score <= 1):
        raise ValueError("Scores must be between 0 and 1")
    return tech_score + sent_score


def main():
    parser = argparse.ArgumentParser(
        description="Fetch technical signal and combine with sentiment score."
    )
    parser.add_argument("--api_key", type=str, required=True, help="Technical analysis API key.")
    parser.add_argument("--sentiment", type=float, required=True, help="Sentiment score (0 to 1).")
    args = parser.parse_args()

    # 1. Fetch technical signal
    rec = get_technical_signal(args.api_key)

    # 2. Compute combined score
    combined_score = decide_position(
        tech_score=rec["tech_score"],
        sent_score=args.sentiment
    )

    # 3. Calculate stop price
    stop_price = rec["price"] * (1 - rec["stop_pct"])

    # 4. Output results
    print(f"Symbol:             {rec['symbol']}")
    print(f"Buy Time:           {rec['buy_time'].isoformat()}")
    print(f"Technical Score:    {rec['tech_score']:.4f}")
    print(f"Sentiment Score:    {args.sentiment:.4f}")
    print(f"Combined Score:     {combined_score:.4f}")
    print(f"Buy Price:          ${rec['price']:.2f}")
    print(f"Stop-Loss Price:    ${stop_price:.2f}")


if __name__ == "__main__":
    main()
