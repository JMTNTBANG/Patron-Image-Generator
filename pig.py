import os
import datetime
import json
import time

# Check for Required Packages
try:
    import dotenv
    from PIL import Image, ImageDraw, ImageFont
    import patreon
except ImportError:
    print("Please run \"poetry install\" before running the script")
    exit(1)

# Import API Token
dotenv.load_dotenv()
token = os.getenv("PATREON")
if token == "":
    print("Please add a Patreon API Key into \".env\" (More Information on how to get a key in \"README.md\")")
    exit(1)


class Patron:
    def __init__(self, data):
        self.tier: str = data.relationship('reward').attribute('title')
        self.created: datetime.datetime = datetime.datetime.fromisoformat(data.attribute('created_at'))
        self.first_name: str = data.relationship('patron').attribute('first_name')
        self.last_name: str = data.relationship('patron').attribute('last_name')
        self.full_name: str = data.relationship('patron').attribute('full_name')
        # self.test = data.


class Config:
    class FontSizes:
        def __init__(self, header1: int, header2: int, member_list: int):
            self.header1: int = header1
            self.header2: int = header2
            self.member_list: int = member_list
    class Loop:
        def __init__(self, enabled: bool, wait_time: int):
            self.enabled: bool = enabled
            self.wait_time: int = wait_time
    def __init__(self, json_file_path):
        self.raw = json.loads(open(json_file_path).read())
        self.tiers: list[str] = self.raw["tiers"]
        self.font_sizes = self.FontSizes(self.raw["font-sizes"]["header1"],
                                         self.raw["font-sizes"]["header2"],
                                         self.raw["font-sizes"]["member-list"])
        self.limit_per_column: int = self.raw["limit-per-column"]
        self.output_directory: str = self.raw["output-directory"]
        self.loop = self.Loop(self.raw["loop"]["enabled"],
                              self.raw["loop"]["wait-time"])


# Error Handling
try:
    config = Config("./config.json")
except FileNotFoundError:
    print("Please Create a config.json File with the code defined in README.md")
    exit(1)
except KeyError as key:
    print(f"Please add {key} entry to .json file as defined in README.md")
    exit(1)
except json.decoder.JSONDecodeError as error:
    print("There has been an unexpected error when reading your config.json file\n\n"
          f"Details: {error}")
    exit(1)
except Exception as error:
    print("Some Unknown Error has happened, please create an issue on GitHub with the following error:\n"
          f"\"{error}\"")
    exit(1)

while True:
    pledges = []
    client = patreon.API(token)
    campaign = client.fetch_campaign().data()[0]
    raw_pledges = client.fetch_page_of_pledges(campaign.id(), 999999)
    for pledge in raw_pledges.data():
        pledges.append(Patron(pledge))
    del raw_pledges


    def create(tier):
        output = Image.new("RGB", (1920, 1080), (0, 0, 0))
        try:
            header_fnt = ImageFont.truetype("./fonts/header.ttf", config.font_sizes.header1)
            header_2_fnt = ImageFont.truetype("./fonts/header.ttf", config.font_sizes.header2)
            content = ImageFont.truetype("./fonts/content.ttf", config.font_sizes.member_list)
        except OSError:
            print("Please Provide Font Files \"header.ttf\" and \"content.ttf\" in fonts folder")
            exit(1)
        d = ImageDraw.Draw(output)
        _, _, w, _ = d.textbbox((0, 0), "Thanks to our Patrons!!", font=header_fnt, align="center")
        d.text(((1920 - w) / 2, 0), "Thanks to our Patrons!!", font=header_fnt, fill=(255, 255, 255), align="center")

        _, _, w, _ = d.textbbox((0, 100), tier+"s", font=header_2_fnt, align="center")
        d.text(((1920 - w) / 2, 150), tier+"s", font=header_2_fnt, fill=(255, 255, 255), align="center")
        members = []
        amt = 0
        current_members = ""
        for pledge in pledges:
            if pledge.tier == tier:
                current_members += f"\n{pledge.full_name}\n{pledge.created.strftime('Joined %m/%d/%Y')}\n"
                amt += 1
                if amt == config.limit_per_column:
                    members.append(current_members)
                    current_members = ""
                    amt = 0
        if amt < config.limit_per_column:
            members.append(current_members)

        width = 0
        for k in members:
            _, _, w, _ = d.multiline_textbbox((50+width, 200), "\n" + k, font=content, align="center")
            d.text((50+width, 200), "\n" + k, font=content, fill=(255, 255, 255), align="center")
            width = w

        try:
            output.save(f"{config.output_directory}/{tier}.png")
        except FileNotFoundError:
            print("Please Specify a valid output directory in config.json")
            exit(1)
        except Exception as error:
            print("Some Unknown Error has happened, please create an issue on GitHub with the following error:\n"
                  f"\"{error}\"")
            exit(1)


    for tier in config.tiers:
        create(tier)
    if not config.loop.enabled:
        break
    else:
        print("Sleeping...")
        time.sleep(config.loop.wait_time)
