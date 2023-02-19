import argparse
import os
from datetime import datetime

from dotenv import load_dotenv

import kafka


def load_env() -> None:
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path)


def polling(bootstrap_servers: str, topic: str) -> None:
    print(f"Connecting to {bootstrap_servers}...")
    consumer = kafka.KafkaConsumer(bootstrap_servers=bootstrap_servers)
    consumer.subscribe(topic)
    print("Waiting for messages to arrive")
    for message in consumer:
        print(message)


def main() -> None:
    load_env()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--bootstrap-servers",
        type=str,
        default=os.environ["BOOTSTRAP_SERVERS"],
        help="接続するブローカー情報"
    )
    parser.add_argument(
        "-t",
        "--topic",
        type=str,
        required=True,
        help="購読するトピック名"
    )
    args = parser.parse_args()

    try:
        polling(bootstrap_servers=args.bootstrap_servers, topic=args.topic)
    except KeyboardInterrupt:
        print("Bye")
    except Exception as e:
        import traceback

        traceback.print_exc(e)


if __name__ == "__main__":
    main()
