import pandas as pd
import re


class ProcessReviews:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def check_keywords(self):
        """
        adds a column for each keyword.
        0 - the review does not contain the keyword
        1 - the review contains the keyword
        """
        self.df['acne'] = self.df.review_text.str.contains('acne|break.out|breakout|pimple', flags=re.IGNORECASE,
                                                           regex=True).astype(int)
        self.df['blackheads'] = self.df.review_text.str.contains('blackhead|clogged pores', flags=re.IGNORECASE,
                                                                 regex=True).astype(int)
        self.df['dry_skin'] = self.df.review_text.str.contains('dry|irritate|tight|soothing|uncomfortable',
                                                               flags=re.IGNORECASE, regex=True).astype(int)
        self.df['rosacea'] = self.df.review_text.str.contains('rosacea|apparent blood vessels|dialated vessels',
                                                              flags=re.IGNORECASE, regex=True).astype(int)
        self.df['irritated_skin'] = self.df.review_text.str.contains(
            'redness|red.skin|inflam|itch|irritat|sooth|painful|calm|rash', flags=re.IGNORECASE, regex=True).astype(int)
        self.df['atopic_dermatitis'] = self.df.review_text.str.contains('atopic.dermatitis|topic.skin|eczema',
                                                                        flags=re.IGNORECASE, regex=True).astype(int)
        self.df['psoriasis'] = self.df.review_text.str.contains('psoriasis', flags=re.IGNORECASE, regex=True).astype(
            int)
        self.df['sensitive_skin'] = self.df.review_text.str.contains('sensitive|allerg|rash', flags=re.IGNORECASE,
                                                                     regex=True).astype(int)
        self.df['oily_skin'] = self.df.review_text.str.contains('oily|shiny|sebum', flags=re.IGNORECASE,
                                                                regex=True).astype(int)
        self.df['pigmentation'] = self.df.review_text.str.contains('pigment|dark spots|sun.spots|sunspots|acne.scars',
                                                                   flags=re.IGNORECASE, regex=True).astype(int)

    def clean(self) -> pd.DataFrame:
        # remove empty reviews
        self.df.dropna(subset=['review_body', 'review_title'], inplace=True)

        # remove non-alphanumeric characters from the product name
        self.df = self.df['product_name'].str.replace('[^\w\s]', '')

        # join the title and the body of the reviews
        self.df['review_text'] = self.df.review_title + ' ' + self.df.review_body
        self.df.drop(columns=['review_body', 'review_title'], inplace=True)

        # check which reviews contain the keywords
        self.check_keywords()

        # keep only the reviews that contain at least one keyword
        num_kw = 10
        self.df = self.df.loc[(self.df.iloc[:, -num_kw:] != 0).any(axis=1)]

        return self.df

    def write_reviews(self):
        # combine all reviews for a single product (separated by \n)
        agg_reviews = self.df.groupby('product_name')['review_text'].agg(lambda x: '\n'.join(x))

        # replace spaces with "_" in the product name:
        agg_reviews.index = agg_reviews.index.str.split().str.join('_')

        # Write reviews to a file readable by AWS comprehend. One file per product, one review per line.
        for index, value in agg_reviews.items():
            with open(f"{index}.txt", 'w', encoding='utf-8') as f:
                f.write(value)


if __name__ == '__main__':

    reviews = pd.read_csv('database.csv')

    process = ProcessReviews(reviews)

    cleaned_reviews = process.clean()
    process.write_reviews()

