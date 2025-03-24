import streamlit as st #for interface
import numpy as np #to help me with arrays
from collections import Counter
from PIL import Image

class Upload:

    #initialize the program
    def __init__(self):
        try:
            st.title("Extract your colors")
            self.file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
            self.image = None
            self.input = st.text_input("Number of colors: ", value="10" ).strip()
        except Exception:
            st.write(":red[Format Unsupported]")

    #open uploaded file
    def openfile(self):
        if self.file is not None:
            self.image = Image.open(self.file)
            st.image (self.image, caption="Uploaded Image", use_container_width=True)
        else:
            st.write(":red[Please Enter a File]")

        return self.image

    #convert the image into arrays
    def convert(self):
        if self.image is not None:
            try:
                self.array = np.asarray(self.image)

                #flatten the array
                flat_array = self.array.reshape(-1,3)

                filtered_color = []
                for color in flat_array:
                    if 50 < 0.2126*color[0] + 0.7152*color[1] + 0.0722*color[2] < 225:
                        filtered_color.append(color)

                #get the frequency
                frequency = Counter(map(tuple, filtered_color))

                dominant_colors = [color for color,_ in frequency.most_common(int(self.input))]
                return dominant_colors
            except ValueError:
                st.write(":red[Please Enter only an Integer]")
    #create tones
    def show_palette(self, dominant_colors):
        tones = []
        try:
            for color in dominant_colors:
                    tones.append(color)
            for tone in tones:
                hex_color = "#{:02x}{:02x}{:02x}".format(*tone)
                st.subheader(f'{hex_color} {tone}')
                st.markdown(f"""
                        <div style='width:100px; height:50px; background:{hex_color};'></div>
                        """,
                        unsafe_allow_html=True
                    )
            return hex_color
        except TypeError:
             st.write(":red[Please Enter only an Integer]")

def main():

    uploaded_file = Upload()
    img = uploaded_file.openfile()
    if img is not None:
        img_arrays = uploaded_file.convert()
        nine_tones = uploaded_file.show_palette(img_arrays)
        print(nine_tones)

if __name__ == "__main__":
    main()
