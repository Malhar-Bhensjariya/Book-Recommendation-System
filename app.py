import pickle
import streamlit as st
import numpy as np

st.header("Books Recommender System using Machine Learning")
model = pickle.load(open('artifacts/model.pkl', 'rb'))
books_name = pickle.load(open('artifacts/books_name.pkl', 'rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))

def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []
    
    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])
        
    for name in book_name[0]:
        ids = np.where(final_rating['Title'] == name)[0][0]
        ids_index.append(ids)
    
    for idx in ids_index:
        url = final_rating.iloc[idx]['img_url']
        poster_url.append(url)
        
    return poster_url
    

def recommend_books(book_name):
    book_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(
        book_pivot.iloc[book_id,:].values.reshape(1,-1), 
        n_neighbors=6)
    poster_url = fetch_poster(suggestion)
    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books:
            book_list.append(j)
    return book_list, poster_url
    

selected_books = st.selectbox(
    "Type or select a book",
    books_name
)

if st.button('Show recommendation'):
    # Load recommendations based on the selected book
    recommendation_books, poster_url = recommend_books(selected_books)
    
    # Display selected book
    coll = st.columns(3)
    with coll[0]:
        st.image(poster_url[0], use_column_width=True)
    with coll[1]:
        st.write(recommendation_books[0])
    
    # Display recommendations in card-like format
    st.subheader("Recommended Books")
    columns = st.columns(5)
    
    for i, col in enumerate(columns):
        with col:
            # Create a card-like layout for each recommended book
            st.image(poster_url[i+1], use_column_width=True)
            st.write(recommendation_books[i+1])
