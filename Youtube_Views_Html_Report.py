from googleapiclient.discovery import build
from prettytable import PrettyTable
import pandas as pd
import plotly.graph_objects as go
import video_functions as vf


# Build a service object for interacting with the API
from api_keys import google_api_key # You can delete this line when you use you own google API key.
youtube = build('youtube', 'v3', developerKey=google_api_key) # Replace google_api_key by your own key

# Youtube Channels ID for selection
channels = {"Ivan_On_Tech": "UCrYmtJBtLdtm2ov84ulV-yg", "Alex_Becker":"UCKQvGU-qtjEthINeViNbn6A",
            "Elio_Trades":"UCMtJYS0PrtiUwlk6zjGDEMA", "Coin_Bureau":"UCqK_GSMbpiV8spgD3ZGloSw",
            "Crypto_Casey":"UCi7RBPfTtRkVchV6qO8PUzg"}

# Start Menu Logic
channel_key_list = list(channels.keys())
for i, key in enumerate(channel_key_list, start=1):
    print(f"{i}.{key}")

while True:
    try:
        choice = int(input("Please select a Youtube channel by entering the corresponding number:"))
        if 1 <= choice <= len(channel_key_list):
            selected_key = channel_key_list[choice-1]
            print(f"You selected: {selected_key}")
            break
        else:
            print(f"Invalid choice. Please select a number between 1 and {len(channel_key_list)}")
    except ValueError:
        print("Invalid Input. Please enter a number")


channel_id = channels[selected_key]
uploads_playlist_id = vf.get_uploads_playlist_id(channel_id, youtube)
videos = vf.list_uploaded_videos(uploads_playlist_id, youtube)

# Use Pretty Table for tabular format
table = PrettyTable()
table.field_names = ["No.", "Title", "Video ID", "Views", "Published On"]

# Print video titles, IDs, and view counts
for i, video in enumerate(videos, start=1):
    table.add_row([i, video['Title'], video['Video ID'], video['Views'], video['Published On']])

print(table)

# Convert the list of dictionaries into a pandas DataFrame
df = pd.DataFrame(videos)

# Plotting with Plotly

df['Moving Average 7'] = df['Views'].rolling(window=7).mean()
df['Moving Average 3'] = df['Views'].rolling(window=3).mean()

fig = go.Figure()

# Add the original views time series
fig.add_trace(go.Scatter(x=df['Published On'], y=df['Views'], mode='lines+markers', name='Views'))

# Add the moving average line
fig.add_trace(go.Scatter(x=df['Published On'], y=df['Moving Average 7'], mode='lines', name='Moving Average 7'))
fig.add_trace(go.Scatter(x=df['Published On'], y=df['Moving Average 3'], mode='lines', name='Moving Average 3'))


# Update layout for better readability
fig.update_layout(title={"text":f'{selected_key} Youtube Channel Views Over Time','y':0.9,'x':0.5,"xanchor":"center", "yanchor":"top",},xaxis_title='Publication Date', yaxis_title='Number of Views', xaxis_tickangle=-45)

# Save the plot as an HTML file
fig.write_html(f'{selected_key}.html')

# Display the plot if running in an interactive environment (like Jupyter Notebook)
# fig.show()

