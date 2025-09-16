# Fund Management Tools

This directory contains 32 Python tool files for managing a fund management database system.

## CUD Operations (Create, Update, Delete):
1. onboard_investor.py - Creates new investor profiles
2. offboard_investor.py - Archives investor data
3. create_fund.py - Creates new funds
4. update_fund.py - Modifies fund details
5. close_fund.py - Closes funds
6. create_subscription.py - Processes subscription requests
7. process_redemption.py - Processes redemption requests
8. execute_trade.py - Executes trades
9. switch_funds.py - Moves investments between funds
10. create_commitment.py - Records investor commitments
11. fulfill_commitment.py - Updates commitment status
12. create_upload_document.py - Creates document records
... and more

## Read Operations:
22. get_investor_profile.py - Retrieves investor information
23. get_fund_info.py - Retrieves fund information
24. get_portfolio_holdings.py - Retrieves portfolio holdings
... and more

Each tool follows the same pattern:
- Implements invoke() method for execution
- Implements get_info() method for schema definition
- Handles validation and error cases
- Returns JSON responses
- Uses consistent ID generation and timestamping
