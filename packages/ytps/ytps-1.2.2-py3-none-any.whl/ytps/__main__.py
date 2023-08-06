def ytps():
	# from __future__ import unicode_literals
	from youtube_search import YoutubeSearch
	from youtubesearchpython import CustomSearch, VideoSortOrder, ChannelsSearch, Search, Video
	from youtubesearchpython import ChannelSearch
	from rich.console import Console
	from rich.panel import Panel
	from rich.progress import Progress
	from rich.prompt import Prompt, Confirm
	from rich.markdown import Markdown
	from rich.table import Table
	from rich import print
	from rich.text import Text
	import requests
	import os
	import webbrowser
	import time
	import argparse
	import youtube_dl

	console = Console()
	parser = argparse.ArgumentParser(prog='Youtube Terminal Play and Search')
	parser.add_argument("search_term", help="Youtube Search Query")
	parser.add_argument('-v','--version', action='version', version='%(prog)s 1.1 : The Search Update')
	parser.add_argument("-o", help="Open Latest Video in mpv", action='store_true')
	parser.add_argument("-c", help="Channel Info", action='store_true')
	parser.add_argument("-p", help="Play the Video Link or First Relevant Video", action='store_true')
	parser.add_argument("--info", help="Video Info", action='store_true')
	parser.add_argument("-l", help="More Relevant Results and more formatting, but slower", action='store_true')
	parser.add_argument("-a", help="About ytps and license", action='store_true')
	parser.add_argument("--download", help="Download the video with search term", action='store_true')
	args = parser.parse_args()

	def shortener(url):
		web_to_visit = f'https://tinyurl.com/api-create.php?url={url}'
		website = requests.get(web_to_visit)
		final_url_raw = str(website.content)
		final_url_semi_raw = final_url_raw.replace("b'", "")
		final_url = final_url_semi_raw.replace("'", "")
		return final_url

	def search_yt(search_term):
		if args.o:
			customSearch = CustomSearch(search_term, VideoSortOrder.uploadDate, limit = 1)
			latest_video = customSearch.result()
			console.print(f':new: Latest Video from {latest_video["result"][0]["channel"]["name"]}')
			console.print(f'{latest_video["result"][0]["title"]} released {latest_video["result"][0]["publishedTime"]}.')
			play_video = Confirm.ask("Do you want to play in mpv")
			if play_video:
				try:
					os.system(f'mpv --fullscreen --no-terminal --title="ytps - Playing {latest_video["result"][0]["title"]} from {latest_video["result"][0]["channel"]["name"]}"  {latest_video["result"][0]["link"]}')
				except:
					webbrowser.open(f'https://www.youtube-nocookie.com/embed/{custom_play_search_content["result"][0]["id"]}')
			quit()

		def speed():
			try:
				import speedtest
				threads = None
				s = speedtest.Speedtest()
				s.get_best_server()
				s.download(threads=threads)
				s.upload(threads=threads)
				s.results.share()
				results_dict = s.results.dict()
				speed_results = {
				"download": f'{str(int(results_dict["download"])// 1000000)} mb/s',
				"upload": f'{str(int(results_dict["upload"])// 1000000)} mb/s',
				"ping": f'{str(results_dict["ping"])} ms'
				}
				return speed_results
			except:
				speed_results = {
				"download": None,
				"upload": None,
				"ping": None
				}
				return speed_results
		def download(url):
			class MyLogger(object):
			    def debug(self, msg):
			    	with open("ytps.log", "a") as file:
			    		file.write(msg)
			    def warning(self, msg):
			        console.log(msg)
			    def error(self, msg):
			        console.log(msg)
			ydl_opts = {
			    'format': 'best',
			    'logger': MyLogger(),
			}
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			    ydl.download([url])
		if args.download:
			if search_term == "":
				print("Enter a valid search term")
			else:
				console.log(f":green_circle: Downloading Relavant Video for {search_term}")
				result = YoutubeSearch(search_term, max_results=1).to_dict()
				console.log(":green_circle: Retrived Data from YouTube")
				console.log("Your Internet Connection Allows with")
				speed_cli = speed()
				console.log(f'Download: {speed_cli["download"]} | Upload: {speed_cli["upload"]} | Ping: {speed_cli["ping"]}')
				with console.status("Downlading Video...", spinner="clock"):
					url_info = download(f'https://youtu.be/{result[0]["id"]}')

		if args.l:
			table = Table(title=Panel(f'Results for [red]{search_term.capitalize()}'), show_header=True, header_style="bold green")
			table.add_column("Released", style="dim", width=20)
			table.add_column("Title", style="yellow")
			table.add_column("Channel", style="cyan")
			table.add_column("Url", no_wrap=True, style="dim blue")

			results = YoutubeSearch(search_term, max_results=20).to_dict()
			for i in results:
				video_url_for_table = f'https://youtu.be/{i["id"]}'
				channel = i["channel"]
				channelsSearch = ChannelsSearch(channel, limit = 10, region = 'US')
				channelsSearch_content = channelsSearch.result()
				table.add_row(
					i["publish_time"],
					i["title"],
					f'[link={channelsSearch_content["result"][0]["link"]}]{channel}[/link]',
					video_url_for_table,
				)
			table.caption = ":zap: Made by [link=https://newtoallofthis123.github.io/About]NoobScience[/link]"
			console.print(table)
			quit()
		if args.c:
			channel_to_search = args.search_term
			channelsSearch = ChannelsSearch(channel_to_search, limit = 10, region = 'US')
			channelsSearch_content = channelsSearch.result()
			console.print(Panel(f'Details for [red]{channel_to_search.capitalize()}'), justify="center")
			console.print(Panel(f'[green bold]Channel Name: [/] {channelsSearch_content["result"][0]["title"]}\n[green bold]Subscribers: [/] {channelsSearch_content["result"][0]["subscribers"]}\n[green bold]Link: [/] [cyan dim]{shortener(channelsSearch_content["result"][0]["link"])}[/]\n[green bold]Description: [/]{channelsSearch_content["result"][0]["descriptionSnippet"][0]["text"]}\n[green bold]Video Count: [/]{channelsSearch_content["result"][0]["videoCount"]}'), justify="center")
			console.print(":zap: Made by [link=https://newtoallofthis123.github.io/About]NoobScience[/link]", justify="center")
			quit()
		if args.p:
			custom_play_search_term = args.search_term
			if "https://youtu" in custom_play_search_term:
				video_url = args.search_term
				video_info = Video.getInfo(video_url)
				console.print(Panel(f'[cyan]{video_info["title"]}[/]\n\n[green bold]Url: [/]{video_info["link"]}\n[green bold]View Count: [/]{video_info["viewCount"]["text"]}\n[green bold]Channel: [/]{video_info["channel"]["name"]}\n[green bold]Channel Link: [/]{video_info["channel"]["link"]}\n[green bold]Description: \n[/]{video_info["description"]}'), justify="center")
				play_video = Prompt.ask("Continue to Play the Video with mpv[violet](mpv)[/] or open embeded[violet](w)[/] or open in youtube[violet](yt)[/] or quit[violet](q)[/]", choices=["mpv", "w", "yt", "quit"], default="mpv")
				if play_video == "mpv":
					with Progress() as progress:
						task1 = progress.add_task("[green]Loading Player...", total=1000)
						while not progress.finished:
							time.sleep(0.01)
							progress.update(task1, advance=5)
					try:
						os.system(f'mpv --fullscreen --no-terminal --title="ytps - Playing {video_info["title"]} from {video_info["channel"]["name"]}"  {video_info["link"]}')
					except:
						webbrowser.open(f'https://www.youtube-nocookie.com/embed/{video_info["id"]}')
				if play_video == "w":
					try:
						webbrowser.open(f'https://www.youtube-nocookie.com/embed/{video_info["id"]}')
					except:
						webbrowser.open(f'https://youtu.be/{video_info["id"]}')
				if play_video == "yt":
					webbrowser.open(f'https://youtu.be/{video_info["id"]}')
				if play_video == "quit":
					quit()
				console.print(":zap: Made by [link=https://newtoallofthis123.github.io/About]NoobScience[/link]", justify="center")
				quit()
			custom_play_search = CustomSearch(custom_play_search_term, VideoSortOrder.relevance, limit = 1)
			custom_play_search_content = custom_play_search.result()
			console.print(Panel(f'Details for [red]{custom_play_search_term.capitalize()}[/]\'s video'), justify="center")
			console.print(Panel(f'[green bold]Most Relevant Video: [/]{custom_play_search_content["result"][0]["title"]}\n[green bold]Url: [/]{custom_play_search_content["result"][0]["link"]}\n[green bold]Channel: [/]{custom_play_search_content["result"][0]["channel"]["name"]}\n[green bold]Duration: [/]{custom_play_search_content["result"][0]["duration"]}\n[green bold]Released: [/]{custom_play_search_content["result"][0]["publishedTime"]}\n[green bold]Views: [/]{custom_play_search_content["result"][0]["viewCount"]["short"]}\n[green bold]Description: [/]{custom_play_search_content["result"][0]["descriptionSnippet"][0]["text"]}'), justify="center")
			play_video = Prompt.ask("Continue to Play the Video with mpv[violet](mpv)[/] or open embeded[violet](w)[/] or open in youtube[violet](yt)[/] or quit[violet](q)[/]", choices=["mpv", "w", "yt", "q"], default="mpv")
			if play_video == "mpv":
				with Progress() as progress:
					task1 = progress.add_task("[green]Loading Player...", total=1000)
					while not progress.finished:
						time.sleep(0.01)
						progress.update(task1, advance=5)
				try:
					os.system(f'mpv --fullscreen --no-terminal --title="ytps - Playing {custom_play_search_content["result"][0]["title"]} from {custom_play_search_content["result"][0]["channel"]["name"]}"  {custom_play_search_content["result"][0]["link"]}')
				except:
					webbrowser.open(f'https://www.youtube-nocookie.com/embed/{custom_play_search_content["result"][0]["id"]}')
			if play_video == "w":
				try:
					webbrowser.open(f'https://www.youtube-nocookie.com/embed/{custom_play_search_content["result"][0]["id"]}')
				except:
					webbrowser.open(f'https://youtu.be/{custom_play_search_content["result"][0]["id"]}')
			if play_video == "yt":
				webbrowser.open(f'https://youtu.be/{custom_play_search_content["result"][0]["id"]}')
			if play_video == "q":
				quit()
			console.print(":zap: Made by [link=https://newtoallofthis123.github.io/About]NoobScience[/link]", justify="center")
			quit()
		if args.info:
			video_url = args.search_term
			video_info = Video.getInfo(video_url) 
			console.print(Panel(f'Details for [red]{video_info["channel"]["name"].capitalize()}[/]\'s video'), justify="center")
			console.print(Panel(f'[cyan]{video_info["title"]}[/]\n\n[green bold]Url: [/]{video_info["link"]}\n[green bold]View Count: [/]{video_info["viewCount"]["text"]}\n[green bold]Channel: [/]{video_info["channel"]["name"]}\n[green bold]Channel Link: [/]{video_info["channel"]["link"]}\n[green bold]Description: \n[/]{video_info["description"]}'), justify="center")
			console.print(":zap: Made by [link=https://newtoallofthis123.github.io/About]NoobScience[/link]", justify="center")
			quit()
		try:
			table = Table(title=Panel(f'Results for [red]{search_term.capitalize()}'), show_header=True, header_style="bold green")
			table.add_column("Released", style="dim", width=20)
			table.add_column("Title", style="yellow")
			table.add_column("Channel", style="cyan")
			table.add_column("Url", no_wrap=True, style="dim blue")

			results = YoutubeSearch(search_term, max_results=20).to_dict()
			for i in results:
				video_url_for_table = f'https://youtu.be/{i["id"]}'
				table.add_row(
					i["publish_time"],
					i["title"],
					i["channel"],
					video_url_for_table,
				)
			table.caption = ":zap: Made by [link=https://newtoallofthis123.github.io/About]NoobScience[/link]"
			console.print(table)
		except:
			for i in results:
				print(f'\n________________________________________\n{i["title"]}\n {i["publish_time"]}\t {i["channel"]}\t {i["duration"]}\t {i["views"]}\n Video Url: https://youtube.com{i["url_suffix"]}\n________________________________________')
			print("Made by NoobScience")

	console.print("\n\t\t:compass:Youtube Search\n", style="bold red", justify="center")
	term_to_search = args.search_term
	search_yt(term_to_search)

if __name__ == '__main__':
	ytps()