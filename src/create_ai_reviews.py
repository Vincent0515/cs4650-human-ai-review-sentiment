from __future__ import annotations

from pathlib import Path

import pandas as pd


POSITIVE_REVIEWS = [
    "This face cream absorbed quickly and left my skin feeling soft without looking greasy. I noticed smoother texture after a few days and would buy it again.",
    "The shampoo has a clean scent and made my hair feel lighter after the first wash. It rinsed out easily and did not leave buildup.",
    "I really liked this moisturizer because it calmed the dry patches on my cheeks. The packaging was simple and the pump worked well.",
    "This lip balm stayed on longer than most of the ones I have tried. It felt comfortable and kept my lips from cracking during the day.",
    "The cleanser removed makeup without making my skin feel tight. I appreciated that it was gentle around my eyes.",
    "This serum gave my skin a brighter look after about a week. It layered well under sunscreen and did not pill.",
    "The body lotion has a pleasant scent that is not too strong. It kept my skin hydrated through the evening.",
    "I bought this for travel and ended up using it every day. The size is convenient and the product works better than expected.",
    "The conditioner made my hair easier to comb and reduced frizz. A small amount was enough for each use.",
    "This sunscreen felt lightweight and did not leave a heavy white cast. It worked well under makeup.",
    "The hand cream helped with dryness after only a few applications. It was rich but still absorbed fast.",
    "I liked the gentle formula and did not experience irritation. It is a good option for my sensitive skin.",
    "The scent is fresh and lasts for several hours without being overwhelming. I received compliments while wearing it.",
    "This exfoliator was effective without feeling harsh. My skin felt smoother but not scratched or red.",
    "The product arrived sealed and in perfect condition. It performed exactly as described and felt high quality.",
    "This hair mask made my ends feel softer after one use. It also made my hair look shinier when it dried.",
    "I was surprised by how well this worked for the price. It feels comparable to more expensive products I have used.",
    "The toner felt refreshing and did not sting. It helped my skin feel cleaner before applying moisturizer.",
    "This mascara added length without clumping. It stayed on during the day and washed off without much effort.",
    "The facial oil felt nourishing and only required a few drops. It gave my skin a healthy glow overnight.",
    "This product fit easily into my routine and gave consistent results. I would recommend it for daily use.",
    "The cream has a smooth texture and spreads evenly. It made my skin feel comfortable during cold weather.",
    "I liked that the fragrance was subtle and clean. It made the product feel pleasant without causing headaches.",
    "The brush is sturdy and easy to hold. It applied product evenly and cleaned up without shedding.",
    "This worked well on my dry elbows and knees. The improvement was noticeable after a couple of nights.",
    "The gel texture felt cooling and absorbed quickly. It was especially nice after being outside in the sun.",
    "I have used this for two weeks and my skin feels more balanced. It did not cause breakouts.",
    "The product is easy to apply and does not feel sticky. It leaves a soft finish that I really like.",
    "This nail treatment helped my nails feel stronger. It dried quickly and did not chip right away.",
    "The cleanser foams nicely and leaves my face feeling fresh. It is gentle enough for morning and night.",
    "I liked the simple ingredient list and the way my skin responded. It felt soothing from the first use.",
    "The deodorant worked through a full workday for me. The scent was light and did not clash with perfume.",
    "This eye cream felt hydrating and did not migrate into my eyes. The small tube lasted longer than expected.",
    "The product gave my hair more volume without making it crunchy. It was easy to style afterward.",
    "This lotion is great after shaving because it does not sting. It leaves my legs smooth and moisturized.",
    "The color matched the online photo closely. It applied smoothly and looked natural.",
    "This product helped reduce the look of dryness around my nose. It felt gentle and reliable.",
    "The packaging was clean and secure, and the product smelled fresh. I had a good experience using it.",
    "This spray refreshed my curls and made them easier to reshape. It did not leave a sticky residue.",
    "I liked the lightweight feel and the smooth finish. It made my morning routine faster.",
    "The mask felt relaxing and left my skin soft afterward. It was easy to rinse off.",
    "This is a dependable product that does what it claims. I would be comfortable purchasing it again.",
    "The texture is creamy but not heavy. It helped my skin stay hydrated during the day.",
    "This powder controlled shine without looking cakey. It worked well for touch-ups.",
    "The product was gentle enough for frequent use. My skin felt clean and calm after using it.",
    "I liked how quickly this showed results on rough skin. It made the area feel smoother by morning.",
    "The scent is soft and pleasant, and the formula feels high quality. It became one of my regular products.",
    "This worked better than I expected on fine hair. It added softness without weighing it down.",
    "The applicator made it easy to use the right amount. The product blended evenly and looked polished.",
    "I am happy with this purchase because it is affordable and effective. It performs well for everyday use.",
]


NEGATIVE_REVIEWS = [
    "This moisturizer felt heavy and left my face shiny for hours. It also caused small breakouts after a few days.",
    "The shampoo made my hair feel dry and tangled. I expected it to be gentle, but it was difficult to rinse out.",
    "The scent was much stronger than I expected and gave me a headache. I could not use it more than once.",
    "This lip balm wore off quickly and did not help with chapped lips. I had to reapply constantly.",
    "The cleanser made my skin feel tight and uncomfortable. It removed makeup poorly and left residue behind.",
    "I did not see any improvement from this serum. It felt sticky and made my sunscreen pill.",
    "The body lotion was watery and not very moisturizing. My skin felt dry again within an hour.",
    "The bottle leaked during shipping and some product was missing. The remaining product also smelled odd.",
    "The conditioner weighed my hair down and made it look greasy. It did not help with frizz at all.",
    "This sunscreen left a noticeable white cast and felt thick. It was hard to blend into my skin.",
    "The hand cream was too greasy for daytime use. It transferred onto everything I touched.",
    "This caused irritation on my sensitive skin. I stopped using it after two applications.",
    "The fragrance faded very quickly and smelled artificial. It was disappointing for the price.",
    "The exfoliator felt rough and left my skin red. It was too harsh for my face.",
    "The product arrived with broken packaging. It did not feel new or properly sealed.",
    "This hair mask made my hair limp instead of soft. It also left a coating that took extra washing to remove.",
    "I expected better quality based on the reviews. The product felt cheap and did not work well.",
    "The toner stung immediately and made my skin look flushed. I would not recommend it for sensitive skin.",
    "This mascara clumped badly and flaked under my eyes. It looked messy by the middle of the day.",
    "The facial oil never fully absorbed and made my face look greasy. It also had an unpleasant smell.",
    "This product did not fit into my routine because it took too long to dry. The results were not worth it.",
    "The cream sat on top of my skin and felt uncomfortable. It did not help with dryness.",
    "The fragrance was overpowering and lingered too long. I had to wash it off.",
    "The brush started shedding after the first wash. Bristles stuck to my face during application.",
    "This did almost nothing for rough skin. I used it several nights and saw no difference.",
    "The gel felt sticky and left a film on my skin. It was not refreshing like I expected.",
    "After two weeks of use, my skin looked the same and felt more congested. I would not repurchase it.",
    "The product was difficult to apply evenly. It dried patchy and looked uneven.",
    "This nail treatment chipped the same day. My nails did not feel stronger after using it.",
    "The cleanser had an unpleasant smell and did not foam well. My face did not feel clean afterward.",
    "The formula sounded simple, but it irritated my skin. I had to stop using it.",
    "The deodorant did not last through a normal workday. I noticed odor again by lunchtime.",
    "This eye cream made the area around my eyes feel puffy. It also burned slightly when applied.",
    "The product made my hair stiff and crunchy. It was hard to brush out later.",
    "This lotion stung after shaving and did not calm my skin. I was disappointed.",
    "The color looked very different from the picture online. It was too orange and hard to blend.",
    "This did not help the dry area around my nose. It actually made the skin feel rougher.",
    "The packaging looked damaged and the product smelled old. I did not feel comfortable using it.",
    "This spray left my curls sticky and weighed down. It made my hair look dull.",
    "The lightweight claim was misleading because it felt tacky all day. I stopped using it after a few tries.",
    "The mask was hard to rinse off and left my skin irritated. It was not relaxing at all.",
    "This product did not do what it claimed. I would not buy it again.",
    "The texture was thick and difficult to spread. It made my skin feel coated rather than hydrated.",
    "This powder looked cakey and settled into lines. It made my makeup look worse.",
    "The product was too drying for frequent use. My skin felt uncomfortable afterward.",
    "I saw no improvement on rough skin. The product felt like ordinary lotion with a higher price.",
    "The scent was unpleasant and the formula felt cheap. I could not finish the bottle.",
    "This made my fine hair look flat and oily. It did not add softness in a useful way.",
    "The applicator dispensed too much product and made a mess. It was frustrating to use.",
    "I regret buying this because it was neither affordable nor effective. It failed for everyday use.",
]


def main() -> None:
    rows = []
    for review in POSITIVE_REVIEWS:
        rows.append({"text": review, "label": "positive", "source": "ai", "rating": ""})
    for review in NEGATIVE_REVIEWS:
        rows.append({"text": review, "label": "negative", "source": "ai", "rating": ""})

    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
    output = Path("data/ai_reviews.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    print(f"Saved {len(df)} AI-generated reviews to {output}")
    print(df["label"].value_counts().to_string())


if __name__ == "__main__":
    main()
