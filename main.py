import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt


def process_data_block(data_block, balance, buy_orders, trades_df):
    profitable_trades = 0
    total_profit = 0
    current_step = None  # Current step (2%, 4%, or 6%)
    buy_count = 0  # Number of purchases in the current step

    data_block = data_block.sort_values(by="open_time")

    unfinished_trades = []  # To store information about unfinished trades

    for index, row in data_block.iterrows():
        open_price = row["open"]
        close_price = row["close"]

        # Buying assets
        if current_step is None or (
            buy_count < 5
            and (
                current_step == -2
                and (not buy_orders or close_price <= buy_orders[-1]["price"] * 0.98)
            )
            or (
                current_step == -4
                and (not buy_orders or close_price <= buy_orders[-1]["price"] * 0.96)
            )
            or (
                current_step == -6
                and (not buy_orders or close_price <= buy_orders[-1]["price"] * 0.94)
            )
        ):
            if current_step is None:
                current_step = -2  # Start with -2%
            else:
                current_step -= 2

            buy_price = open_price
            buy_amount = balance / buy_price
            if buy_amount > 0:
                buy_amount = part_balance / buy_price
                buy_orders.append(
                    {"price": buy_price, "amount": buy_amount, "time": row["open_time"]}
                )
                balance -= buy_price * buy_amount
                buy_count += 1

        completed_orders = []

        for order in buy_orders:
            if close_price >= order["price"] * 1.04:
                profitable_trades += 1
                profit = (close_price - order["price"]) * order["amount"]
                total_profit += profit
                trade_id = len(trades_df) + 1
                trade = {
                    "Buy Price": order["price"],
                    "Buy Amount": order["amount"],
                    "Sell Price": close_price,
                    "Sell Amount": order["amount"],
                    "Profit": profit,
                    "Buy Time": datetime.datetime.fromtimestamp(order["time"] / 1000),
                    "Sell Time": datetime.datetime.fromtimestamp(
                        row["close_time"] / 1000
                    ),
                    "Trade ID": trade_id,
                }
                trades_df = pd.concat(
                    [trades_df, pd.DataFrame([trade])], ignore_index=True
                )
                completed_orders.append(order)

        for order in completed_orders:
            buy_orders.remove(order)

        if buy_orders:
            unfinished_trade = {
                "Buy Price": buy_orders[-1]["price"],
                "Buy Amount": buy_orders[-1]["amount"],
                "Sell Price": None,
                "Sell Amount": None,
                "Profit": None,
                "Buy Time": datetime.datetime.fromtimestamp(
                    buy_orders[-1]["time"] / 1000
                ),
                "Sell Time": None,
                "Trade ID": buy_orders[-1]["time"],
            }
            unfinished_trades.append(unfinished_trade)

    return profitable_trades, total_profit, trades_df, unfinished_trades


def load_data_frames(folder_path):
    data_frames = []
    file_names = os.listdir(folder_path)

    for file_name in file_names:
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            data = pd.read_csv(file_path)
            data_frames.append(data)

    return data_frames


def combine_data_frames(data_frames):
    return pd.concat(data_frames, ignore_index=True)


def main():
    folder_path = "BTCUSDT"
    data_frames = load_data_frames(folder_path)

    initial_balance = 450000
    global part_balance
    num_parts = 15
    part_balance = initial_balance / num_parts

    trades_df = pd.DataFrame(
        columns=[
            "Buy Price",
            "Buy Amount",
            "Sell Price",
            "Sell Amount",
            "Profit",
            "Buy Time",
            "Sell Time",
            "Trade ID",
        ]
    )
    plt.figure(figsize=(15, 8))

    buy_orders = []
    block_size = 100

    combined_data = combine_data_frames(data_frames)
    combined_data = combined_data.sort_values(by="open_time")

    for i in range(0, len(combined_data), block_size):
        data_block = combined_data[i : i + block_size]
        (
            profitable_trades,
            total_profit,
            trades_df,
            unfinished_trades,
        ) = process_data_block(data_block, initial_balance, buy_orders, trades_df)

        print(f"Statistics for data block {i + 1}-{i + block_size}:")
        print(f"Number of profitable trades: {profitable_trades}")
        print(f"Total profit: {total_profit} USD")
        print(f"Total profit percentage: {total_profit / initial_balance * 100} %")

    plt.plot(trades_df["Buy Time"], trades_df["Buy Price"], "ro", label="Buy Price")
    for i, row in trades_df.iterrows():
        plt.text(
            row["Buy Time"],
            row["Buy Price"],
            f"{row['Trade ID']}",
            fontsize=12,
            ha="left",
        )

    plt.plot(trades_df["Sell Time"], trades_df["Sell Price"], "go", label="Sell Price")
    for i, row in trades_df.iterrows():
        plt.text(
            row["Sell Time"],
            row["Sell Price"],
            f"{row['Trade ID']}",
            fontsize=12,
            ha="left",
        )

    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    trades_df.to_csv("trades.csv", index=False)


if __name__ == "__main__":
    main()
