import pandas as pd
from pathlib import PurePath

class PostStorer:
    def __init__(self, storage_folder : PurePath) -> None:
        self.output_dir = storage_folder

    def save_posts(self, new_posts) -> None:
        suffix = f"posts-from-{new_posts[-1]['created']}-to-{new_posts[0]['created']}.csv"
        output_file_path = self.output_dir / suffix

        columns = ["title", "score", "selftext", "created", "author", "url", "timeslot-start", "timeslot-end"]    
        data = [ [p["title"], p["score"], p["selftext"], p["created"], p["author"], p["url"], p["time_slot"][1], p["time_slot"][0]] for p in new_posts]

        df = pd.DataFrame(data, columns = columns)
        df.to_csv(output_file_path, index=False, encoding='utf-8')


    def save_comments(self, new_comments) -> None:
        suffix = f"comments-from-{new_comments[-1]['created']}-to-{new_comments[0]['created']}.csv"
        output_file_path = self.output_dir / suffix
                    
        columns = ["body", "author", "created", "url", "timeslot-start", "timeslot-end"]

        data = [ [c["body"], c["author"], c["created"], c["url"], c["time_slot"][1], c["time_slot"][0]] for c in new_comments]
        df = pd.DataFrame(data, columns = columns)
        df.to_csv(output_file_path, encoding='utf-8', index=False)


if __name__ == "__main__":
    import json
    ps = PostStorer(PurePath("/home/rytis/Desktop/wsb-stonks/reddit-data"))

    with open('/home/rytis/Desktop/wsb-stonks/backend/posts.txt') as f:
        new_posts = json.loads(f.read())
        ps.save_posts(new_posts)

    with open('/home/rytis/Desktop/wsb-stonks/backend/comments.txt') as f:
        new_comments = json.load(f)
        ps.save_comments(new_comments)