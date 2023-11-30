import streamlit as st
import requests

def welcomePage():
    st.markdown("<img style='text-align: center; display: block; margin-left: auto; margin-right: auto; width: 75%; border: 10px solid #bdfbff' src='https://cdn-imgix.headout.com/media/images/a4d93bc58c9528951ed3124f77d268e4-544-amsterdam-003-amsterdam-%7C-rijksmuseum-02.jpg?auto=format&w=814.9333333333333&h=458.4&q=90&fit=crop&ar=16%3A9'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black'>Welcome to the Rijksmuseum!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px'>Use the sidebar on the left to browse through more than a million artworks in our database.</p>", unsafe_allow_html=True)

    
def artist(timePeriod, firstLetter, pieceLetter):
    r = requests.get("https://www.rijksmuseum.nl/api/en/collection?key=63N8gLOd")
    data = r.json()
    artpieceList = []
    for artist in data["facets"][0]["facets"]:
        if artist["key"][0].upper() == firstLetter.upper():
            artistList.append(artist["key"])
    for a in artistList:
        try:
            j = requests.get("https://www.rijksmuseum.nl/api/en/collection?key=63N8gLOd&involvedMaker=" + a + "&f.dating.period=" + str(timePeriod))
            d = j.json()
            for piece in d["artObjects"]:
                if pieceLetter.lower() in piece["title"].lower():
                    artpieceList.append((piece["title"], piece["objectNumber"]))
        except:
            continue
    return artpieceList


def checkTwo(artpieceNums):
    for i, number in enumerate(artpieceNums):
        r = requests.get("https://www.rijksmuseum.nl/api/en/collection/" + number + "?key=63N8gLOd")
        data = r.json()
        error = True
        for item in data['artObject']['makers']:
            if item['name'] in artistList:
                error = error and False
        if error == False:
            artpieceNumsC.append(artpieceNums[i])
            artpieceTitlesC.append(artpieceTitles[i])
        
    
def displayInfo(number):
    r = requests.get("https://www.rijksmuseum.nl/api/en/collection/" + number + "?key=63N8gLOd")
    data = r.json()
    title = data['artObject']['title']
    st.markdown("<h1 style='text-align: center; color: black'>{}</h1>".format(title), unsafe_allow_html=True)
    try:
        url = data['artObject']['webImage']['url']
        st.markdown("<img style='text-align: center; display: block; margin-left: auto; margin-right: auto; width: 75%; border: 10px solid #d1b736; margin-bottom: 20px' src='{}'>".format(url), unsafe_allow_html=True)
    except:
        st.markdown("<img style='text-align: center; display: block; margin-left: auto; margin-right: auto; width: 75%' src='https://st4.depositphotos.com/14953852/24787/v/450/depositphotos_247872612-stock-illustration-no-image-available-icon-vector.jpg'>", unsafe_allow_html=True)
    artist = ""
    for item in data['artObject']['makers']:
        if item['name'] in artistList:
            artist = item['name']
    if artist == "":
        artist = "Can't be found"
    yearMade = data['artObject']['dating']['presentingDate']
    location = ""
    for item in data['artObject']['productionPlaces']:
        location += item + ", "
    location = location[:-2]
    types = ""
    for item in data['artObject']['objectTypes']:
        types += item + ", "
    types = types[:-2]
    techniques = ""
    for item in data['artObject']['techniques']:
        techniques += item + ", "
    techniques = techniques[:-2]
    materials = ""
    for item in data['artObject']['materials']:
        materials += item + ", "
    materials = materials[:-2]    
    st.markdown("<p style='text-align: center; font-size: 20px; color: black'>Artist: {}</p>".format(artist), unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: black'>Year(s) Created: {}</p>".format(yearMade), unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: black'>Location(s) of Production: {}</p>".format(location), unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: black'>Artwork Type(s): {}</p>".format(types), unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: black'>Technique(s): {}</p>".format(techniques), unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: black'>Material(s): {}</p>".format(materials), unsafe_allow_html=True)

def displayErrorMsg():
    st.markdown("<h1 style='text-align: center; color: black'>Sorry, we couldn't find any art pieces that meet those conditions :/</h1>", unsafe_allow_html=True)
    st.markdown("<img style='text-align: center; display: block; margin-left: auto; margin-right: auto; width: 75%' src='https://render.fineartamerica.com/images/images-profile-flow/400/images/artworkimages/mediumlarge/1/focal-point-leon-zernitsky.jpg'>", unsafe_allow_html=True)

st.sidebar.title("Search")
timePeriod = st.sidebar.number_input("Century", min_value=0, max_value=21, value=0, step=1)
firstLetter = st.sidebar.text_input("First Letter of Artist's Name", max_chars=1)
pieceLetter = st.sidebar.text_input("Title Contains Letter:", max_chars=1)


if firstLetter != "" and pieceLetter != "":
    loadingGIF = st.markdown("<img style='text-align: center; display: block; margin-left: auto; margin-right: auto; width: 75%' src='https://cdn.dribbble.com/users/11609495/screenshots/18251844/media/a4d3556d8b51796968cbcc63ea7c5abc.gif'>", unsafe_allow_html=True)
    artistList = []
    artpieceList = artist(timePeriod, firstLetter, pieceLetter)
    artpieceTitles = []
    artpieceNums = []
    artpieceTitlesC = []
    artpieceNumsC = []
    for title, num in artpieceList:
        artpieceTitles.append(title)
        artpieceNums.append(num)
    checkTwo(artpieceNums)
    try:
        artPiece = st.sidebar.radio("Choose an Art Piece", artpieceTitlesC)
        index = artpieceTitlesC.index(artPiece)
        number = artpieceNumsC[index]
        loadingGIF.empty()
        displayInfo(number)
    except:
        loadingGIF.empty()
        displayErrorMsg()
else:
    welcomePage()





                
                
