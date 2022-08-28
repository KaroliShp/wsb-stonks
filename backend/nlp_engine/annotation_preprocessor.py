import pandas as pd
import pathlib
import jsonlines

class AnnotationPreprocessor:
    def __init__(self, RAW_DIR : pathlib.Path, OUTPUT_DIR_FOR_ANNOTATIONS : pathlib.Path) -> None:
        self.RAW_DIR = RAW_DIR
        self.OUTPUT_DIR_PREANNOTATION = OUTPUT_DIR_FOR_ANNOTATIONS

    def get_output_file_name(self, raw_file_stem):
        return self.OUTPUT_DIR_PREANNOTATION / f"{raw_file_stem}.jsonl"
    
    def save_in_annotation_format(self) -> None:
        for fp in self.RAW_DIR.iterdir():
            # check that annotation file hasn't yet been created
            if self.get_output_file_name(fp.stem) in self.OUTPUT_DIR_PREANNOTATION.iterdir():
                pass
            else:
                # preprocess for annotating
                if fp.stem.startswith("comments"):
                    df = pd.read_csv(str(fp))
                    df["text"] = df["body"]
                elif fp.stem.startswith("posts"):
                    df = pd.read_csv(str(fp))
                    # a lot of posts don't have text, just a memey image 
                    df["selftext"] = df["selftext"].fillna("")
                    # put title and selftext together
                    df["text"] = df[["title", "selftext"]].agg('. '.join, axis=1)
                self._save_as_JSONLines(df, self.get_output_file_name(fp.stem))
    
    def _save_as_JSONLines(self, df, output_path) -> None:
        json_list = []

        for idx in df.index:
            row_json = df.iloc[idx].to_dict()
            row_json["label"] = []
            json_list.append(row_json)
        
        with jsonlines.open(output_path, mode='w') as writer:
            writer.write_all(json_list)


if __name__ == "__main__":
    RAW_DIR = pathlib.Path("/home/rytis/Desktop/wsb-stonks/reddit-data/raw")
    ANNOTATION_DATA_PATH = pathlib.Path("/home/rytis/Desktop/wsb-stonks/reddit-data/for-annotation")

    anot_preproc = AnnotationPreprocessor(RAW_DIR, ANNOTATION_DATA_PATH)
    anot_preproc.save_in_annotation_format()
