import argparse
import logging
import requests
import ast
from handle_bulk_data import store_into_redis,fetch_data
from sanic import Sanic, response
from sanic.response import json

logger = logging.getLogger(__name__)

DEFAULT_SERVER_PORT = 6969

DEFAULT_SANIC_WORKERS = 250


def create_argument_parser():
    """Parse all the command line arguments for the redis server script."""

    parser = argparse.ArgumentParser(description="starts the redis endpoint")
    parser.add_argument(
        "-p",
        "--port",
        default=DEFAULT_SERVER_PORT,
        type=int,
        help="port to run the server at",
    )
    parser.add_argument(
        "--workers",
        default=DEFAULT_SANIC_WORKERS,
        type=int,
        help="Number of processes to spin up",
    )

    return parser


async def generate_response(nlg_call):
    customer_details=nlg_call
    print("customer_details",customer_details)
    store_into_redis(customer_details['data'])
    status = "done"
    return status

async def generate_response_1(nlg_call):
    customer_details=nlg_call
    print("customer_details",customer_details)
    data=fetch_data(customer_details['data'])
    return data
    # return bot_response


def run_server(port, workers):
    app = Sanic(__name__)

    @app.route("/push_to_redis", methods=["POST", "OPTIONS"])
    async def nlg(request):
        """Endpoint which processes the Core request for a bot response."""
        nlg_call = request.json
        print("NLG Response", nlg_call)
        bot_response = await generate_response(nlg_call)
        return json({'message': bot_response})

    @app.route("/get_data_redis", methods=["POST", "OPTIONS"])
    async def nlg(request):
        """Endpoint which processes the Core request for a bot response."""
        nlg_call = request.json
        print("NLG Response", nlg_call)
        bot_response = await generate_response_1(nlg_call)
        return json({'message': bot_response})

        
    app.run(host="0.0.0.0", port=port, workers=workers)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Running as standalone python application
    arg_parser = create_argument_parser()
    cmdline_args = arg_parser.parse_args()

    run_server(cmdline_args.port, cmdline_args.workers)
