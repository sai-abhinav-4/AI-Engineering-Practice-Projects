from langchain_text_splitters import RecursiveCharacterTextSplitter

your_long_document = """# Bengaluru Overview
Bengaluru, also known as Bangalore, is the capital of India's southern Karnataka state and is widely regarded as the Silicon Valley of India.

## Tech Overview
The city is India's leading information technology exporter and hosts thousands of tech startups alongside multinational giants like Infosys, Wipro, Google, and Microsoft. Electronic City and Whitefield are major technological hubs teeming with software engineers and product innovators.

## Climate
Bengaluru enjoys a pleasant, moderate climate throughout the year due to its high elevation of approximately 920 meters above sea level. Summers are warm and breezy, while winters are mild and rarely dip below 15 degrees Celsius.

## Food
The city boasts a rich culinary culture ranging from traditional South Indian breakfast joints serving crispy masala dosas, steaming idlis, and filter coffee in classic Darshinis, to an eclectic mix of international dining and vibrant craft microbreweries.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=80,        # aim for ~800 chars per chunk
    chunk_overlap=10,     # adjacent chunks share 100 chars (context glue)
)

chunks = splitter.split_text(your_long_document)
print(chunks)
print(len(chunks))    # → e.g. 47 chunks ready to embed
