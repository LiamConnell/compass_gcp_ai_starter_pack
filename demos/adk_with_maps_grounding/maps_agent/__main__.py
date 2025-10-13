import asyncio
import sys
import json
import argparse
from .run_agent import run_agent


async def main():
    parser = argparse.ArgumentParser(description="Run the maps agent")
    parser.add_argument("query", help="The query to send to the agent")
    parser.add_argument("--output", "-o", help="Output file to write JSON results to")
    
    args = parser.parse_args()
    
    events = await run_agent(args.query)
    
    if args.output:
        # Convert events to serializable format
        events_data = []
        for event in events:
            event_dict = event.model_dump() if hasattr(event, 'model_dump') else str(event)
            events_data.append(event_dict)
        
        with open(args.output, 'w') as f:
            json.dump(events_data, f, indent=2, default=str)
        print(f"Results written to {args.output}")
    else:
        for event in events:
            print(f"Event: {event}")


if __name__ == "__main__":
    asyncio.run(main())