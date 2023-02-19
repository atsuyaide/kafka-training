import argparse
import os
from typing import Optional

from dotenv import load_dotenv

import kafka


def load_env() -> None:
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path)


def print_recived_message(bootstrap_servers: str, topic: str, group_id: Optional[str]) -> None:
    print(f"Connecting to {bootstrap_servers}...")
    consumer = kafka.KafkaConsumer(
        bootstrap_servers=bootstrap_servers, group_id=group_id
    )
    consumer.subscribe([topic])
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
        help="接続するブローカーの情報",
    )
    parser.add_argument("-t", "--topic", type=str, required=True, help="購読するトピック名")
    parser.add_argument(
        "-g", "--group-id", type=str, default="sample-group-id", help="グループID"
    )
    args = parser.parse_args()

    try:
        print_recived_message(
            bootstrap_servers=args.bootstrap_servers,
            topic=args.topic,
            group_id=args.group_id,
        )
    except KeyboardInterrupt:
        print("Bye")
    except Exception as e:
        import traceback

        traceback.print_exc(e)


if __name__ == "__main__":
    main()
