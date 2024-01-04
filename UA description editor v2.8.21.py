# Created on 20 / 06 / 2023
# Arvin Dev

import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
from tkinter import scrolledtext

class UADescriptionEditor:
    """Class representing the Main Window
    """
    def __init__(self, root):
        """Initialiser method for the Main window

        Args:
            root (tk.Tk): tk.Tk Instance to use
        """
        self._root = root
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=2)

        root.rowconfigure(0, weight=1)     
        #self._root.state('zoomed') # Full-screen :3
        HEIGHT = "510"
        WIDTH = "770"
        self._root.geometry(f"{WIDTH}x{HEIGHT}")
        self._root.title("UA Description Editor v2.8.21")
        ibm_mainframe = tk.Canvas(root)
        
        ibm_mainframe.pack_propagate(False)
        # Create a canvas widget
        canvas = tk.Canvas(ibm_mainframe)
        
        self._canvas = canvas
        # Add a scrollbar to the canvas
        scrollbar = ttk.Scrollbar(canvas, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._scrollbar = scrollbar
        
        # Configure the canvas to use the scrollbar
        canvas.config(yscrollcommand=scrollbar.set)
        
        # Create a frame inside the canvas to hold the content -- Frame [2]
        frame = tk.Frame(canvas)
        
        
        self._frame = frame
        # Product Name Entry
        product_name_label = ttk.Label(frame, text="Enter Product Name: ")
        product_name_label.pack(side=tk.TOP)
        self._product_name_entry = ttk.Entry(frame, font=("TkDefaultFont", 12))
        self._product_name_entry.pack(side=tk.TOP, fill=tk.X)
        
        # Subheading Entry
        subheading_label = ttk.Label(frame, text="Enter Sub Heading: ")
        subheading_label.pack(side=tk.TOP)
        self._subheading_entry = tk.Entry(frame, font=("TkDefaultFont", 12))
        self._subheading_entry.pack(side=tk.TOP, fill=tk.X)
        
        # Description ScrolledText Entry
        description_label = ttk.Label(frame, text="Enter Description: ")
        description_label.pack(side=tk.TOP)
        self._description_text = scrolledtext.ScrolledText(frame, height=7, font=("TkDefaultFont", 12))
        self._description_text.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
        description_text = ttk.Sizegrip(self._description_text) 
        description_text.pack(side="bottom", anchor="se") 
        
        # Main features Entry
        features_label = ttk.Label(frame, text="Enter Features: ")
        features_label.pack(side=tk.TOP)
        self._features_text = scrolledtext.ScrolledText(frame, height=7, font=("TkDefaultFont", 12))
        self._features_text.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
        features_text_drag  = ttk.Sizegrip(self._features_text)
        features_text_drag.pack(side="bottom", anchor="se")

        self._features_text.bind("<Tab>", lambda event: self.next_widget(event))
        self._description_text.bind("<Tab>", lambda event: self.next_widget(event))

        button_frame = tk.Frame(frame)
        button_frame.pack(side=tk.BOTTOM, expand=tk.TRUE, fill=tk.X)
        clear_reset_frame = ttk.Frame(button_frame)
        clear_reset_frame.pack(side=tk.BOTTOM,fill=tk.X)
        
        # Clear all but without subfeatures button
        reset_button = tk.Button(clear_reset_frame, text="Reset", command=self.clear_to_default, relief=tk.RAISED, borderwidth=2, bg="pink")
        reset_button.pack(side=tk.RIGHT, fill=tk.X, expand=tk.TRUE)
        
        # Clear all entries button
        clear_button = tk.Button(clear_reset_frame, text="Clear All", command=self.clear_all, relief=tk.RAISED, borderwidth=2, bg="pink")
        clear_button.pack(side=tk.RIGHT, fill=tk.X, expand=tk.TRUE)
        
        # Convert to HTML button
        enter_button = tk.Button(button_frame, text="Create HTML", command=self.text_to_html, relief=tk.RAISED, borderwidth=2, bg="light green", height=2)
        enter_button.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add embedded Button
        self._add_embedded = tk.Button(button_frame, text="Add Embedded", command=self.add_embedded, relief=tk.RAISED, borderwidth=2, bg="light blue")
        self._add_embedded.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add sub-feature Button
        add_sub = tk.Button(button_frame, text="Add Sub Feature", command=self.add_sub_feat, relief=tk.RAISED, borderwidth=2, bg="#CBC3E3")
        add_sub.pack(side=tk.BOTTOM, fill=tk.X)
        
        self._sub_feat_label = False # Sentinel values
        self._embedded_label = False
        
        # Add the frame to the canvas
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)
        
        
        # Configure the canvas to resize with the window
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        frame.pack(expand=tk.TRUE, fill=tk.BOTH, side=tk.TOP)
        frame.pack_propagate(False)
        ibm_mainframe.pack(fill=tk.BOTH, expand=tk.TRUE)
        frame.pack_propagate(False)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE, anchor=tk.NW)
        self._sub_feats = []
        self._embeds = []
    def next_widget(self, event):
        """Logic for tab functionality so when tab is actually pressed for
        scrolled texts it will actually go to next box instead of adding an indent.

        Args:
            event (event): the event that is being passed

        Returns:
            str: break to indicate to not add indent.
        """
        current_widget = self._root.focus_get()  # Get the currently focused widget

        if current_widget == self._description_text:
            self._features_text.focus_set() 
        elif (current_widget == self._features_text):
            if (len(self._sub_feats) != 0):
                title, description = self._sub_feats[0]
                title.focus_set() 
        elif (current_widget in self._embeds):
            current = self._embeds.index(current_widget)
            try:
                next_widget = self._embeds[0]
            except (IndexError):
                next_widget = current_widget
            next_widget.focus_set()
        else:
            # Find the current sub-feature entry and focus the next one
            next_widget = None
            for i, (title, description) in enumerate(self._sub_feats):
                if current_widget == description:
                    try:
                        title, text = self._sub_feats[i+1]
                        next_widget = title
                    except (IndexError):
                        if (len(self._embeds) != 0):
                            next_widget = self._embeds[-1]
                        else:
                            next_widget = current_widget
                    break
            if next_widget is None:
                next_widget = self._root.tk_focusNext()

            next_widget.focus_set() 

        return "break"  # Prevent default behavior of the Tab key
    def clear_to_default(self):
        """Reset to the original state of the program.
        clear_to_default() deletes all the extra subfeatures.
        """
        # Will delete all values in the entry boxes
        self._product_name_entry.delete(0, tk.END)
        self._subheading_entry.delete(0, tk.END)
        self._description_text.delete(1.0, tk.END)
        self._features_text.delete(1.0, tk.END)
        # Destroys and unpacks all the sub feature titles and feature boxes.
        for title, feature in self._sub_feats:
            title.destroy()
            feature.destroy()
            feature.vbar.destroy()
            title.pack_forget()
            feature.pack_forget()
        for embed in self._embeds:
            embed.destroy()
            embed.vbar.destroy()
            embed.pack_forget()
        # Deletes and resets labels and values.
        if (self._sub_feat_label):
            self._sub_feat_label.destroy()
            self._sub_feat_label = False
        if (self._embedded_label):
            self._embedded_label.destroy()
            self._embedded_label = False
        self._sub_feats.clear()
        self._embeds.clear()
        self._canvas.update_idletasks()
        self._canvas.config(scrollregion=self._canvas.bbox("all"))
    def clear_all(self):
        """Clear all the information in the entries/Text boxes,
        but does not delete any extra added subfeatures boxes, etc.
        """
        self._product_name_entry.delete(0, tk.END)
        self._subheading_entry.delete(0, tk.END)
        self._description_text.delete(1.0, tk.END)
        self._features_text.delete(1.0, tk.END)
        for title, feature in self._sub_feats:
            title.delete(0, tk.END)
            feature.delete(1.0, tk.END)
        for embeds in self._embeds:
            embeds.delete(1.0, tk.END)
    def add_sub_feat(self):
        """ To create the subfeature heading and main text upon button click.
        """
        # Enter Sub-features label to show up on first time clicked
        if self._sub_feat_label == 0:
            self._sub_feat_label = tk.Label(self._frame, text="Enter Sub-features: ")
            self._sub_feat_label.pack(side=tk.TOP)
        
        
        # Enter the Heading and dot-points for the subfeatures
        sub_feat_title = tk.Entry(self._frame, font=("TkDefaultFont", 12))
        sub_feat_title.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE, pady=5)
        sub_feat_text = scrolledtext.ScrolledText(self._frame, font=("TkDefaultFont", 12), height=5)
        sub_feat_text.pack(side=tk.TOP, expand=tk.TRUE)
        sub_feat_text.bind("<Tab>", lambda event: self.next_widget(event))
        
        self._sub_feats.append((sub_feat_title, sub_feat_text)) # Add to list to be used later
        self._canvas.update_idletasks()
        self._canvas.config(scrollregion=self._canvas.bbox("all"))
    def add_embedded(self):
        """_summary_
        """
        
        # TextBox for HTML code to go into.
        embeddedTextbox = scrolledtext.ScrolledText(self._frame, font=("TkDefaultFont", 12), height=5)
        embeddedTextbox.pack(side=tk.BOTTOM, expand=tk.TRUE)
        embeddedTextbox.bind("<Tab>", lambda event: self.next_widget(event))
        
        if (self._embedded_label is not False):
            self._embedded_label.destroy()
            
        self._embedded_label = tk.Label(self._frame, text="Enter Embedded: ")
        self._embedded_label.pack(side=tk.BOTTOM)
        
        self._embeds.append(embeddedTextbox) # Add to list to be used later
        self._canvas.update_idletasks()
        self._canvas.config(scrollregion=self._canvas.bbox(tk.ALL))
    def text_to_html(self):
        """ Formats, converts and handles converting the text inputted into the
        correct HTML syntax.
        """
        # Product Name conversion
        product_name = self._product_name_entry.get()
        product_name = product_name.strip()
        all_text = ""
        if product_name != "":  # If there is a product name inputted then add to HTML.
            product_name_html = f"""<h3 style="font-size: 11pt; font-family: helvetica; align-items: left;"><strong>{product_name}</strong></h3>\n"""
        else:
            product_name_html = ""
        
        # Subheading conversion
        subheading = self._subheading_entry.get()
        subheading = subheading.strip().upper()
        if subheading != "":
            subheading_html = f"""<h4 style="font-size: 9pt; font-family: helvetica; padding-top: 10px; font-weight: bold; color: #636363;">{subheading}</h4>\n"""
        else:
            subheading_html = ""
        
        # Description Conversion
        description = self._description_text.get("1.0", tk.END)
        description = description.replace('\n', ' ')
        description = description.strip()
        if description != "":
            description_html = f"""<p style="font-size: 11pt; font-family: helvetica; line-height: 1.6; text-align: justify; color: black">{description}</p>\n"""
        else:
            description_html = ""
        
        # Check if there are any subfeatures, if not add piece of html
        entry = False
        for i, j in self._sub_feats: # = > (i, j == text, title)
            title = i.get().strip()
            text = j.get("1.0", tk.END)
            text = text.strip()
            if title != "":
                entry = True
        if entry == False:
            features_margin =  """ margin-bottom: -4px"""
        else:
            features_margin = ""
        
        # Features Conversion
        features = self._features_text.get("1.0", tk.END)
        features_html = self.convert_descr_to_html(features)
        if subheading_html == "" and description_html == "": #if subheading & description is empty, then add some padding
            features_html = f"""<ul style="list-style-type: disc; padding-left: 20; line-height: 1.6; margin-top: -5px; padding-top: 13px;{features_margin}">""" + "\n" + features_html
        elif description_html != "": #if description has something in it, then no padding
            features_html = f"""<ul style="list-style-type: disc; padding-left: 20; line-height: 1.6; margin-top: -5px;{features_margin}">""" + "\n" + features_html
        elif subheading_html != "":
            features_html = f"""<ul style="list-style-type: disc; padding-left: 20; line-height: 1.6; margin-top: 5px;{features_margin}">""" + "\n" + features_html
        elif features_html != "":
            features_html = f"""<ul style="list-style-type: disc; padding-left: 20; line-height: 1.6; margin-top: -5px;{features_margin}">""" + "\n" + features_html
        else:
            features_html = ""

        # Collates them into all_text which represents the final version
        all_text = product_name_html + subheading_html + description_html + features_html  
        
        if self._sub_feats != []: # Checks if all are empty so that the <\ul> needs to be added or not.
            saved = ""
            for first, _ in self._sub_feats:
                first = first.get().title()
                if first:
                    saved = first.strip()
                else:
                    pass
            all_text = all_text.strip()
            for title, text in self._sub_feats:
                title = title.get().title().strip()
                text = text.get("1.0", tk.END)
                text = text.strip()
                if title: # Only do this if title is given
                    all_text += "\n</ul>\n"
                    all_text = all_text + f"""<h5 style="font-size: 11pt; font-family: helvetica; line-height: 1.6;"><strong>{title}</strong></h5>"""
                    if title == saved:
                        all_text = all_text + "\n" + """<ul style="list-style-type: disc; padding-left: 20; padding-top: 4px; margin-top: -3px; line-height: 1.6; margin-bottom: -4px;">"""
                    else:
                        all_text = all_text + "\n" + """<ul style="list-style-type: disc; padding-left: 20; padding-top: 4px; margin-top: -3px; line-height: 1.6;">"""
                    text = self.convert_descr_to_html(text)
                    if text == "":
                        all_text = all_text + "\n</ul>\n"
                    else:
                        all_text = all_text + "\n" + text +"\n</ul>"

        all_text = all_text.strip()
        all_text += "\n"

        for code in self._embeds:
            all_text += (code.get("1.0", tk.END).strip() + "\n")
        all_text = all_text.strip()

        response = messagebox.showinfo("Copy Text", "HTML Generated\n\nPress OK to copy text", icon="info", type="okcancel")
        if response == "ok":
            self._root.clipboard_clear()
            self._root.clipboard_append(all_text)
        else:
            pass
    def convert_descr_to_html(self, text):
        """ given text from tk.Text, where each line is a bullet point, it will convert each
        line to html code suitable for bullet points.
        
        >>> convert_descr_to_html("hi\nhow\nare\nyou?")
        
            <li style="font-size: 11pt; font-family: helvetica;">hi</li>
            <li style="font-size: 11pt; font-family: helvetica;">how</li>
            <li style="font-size: 11pt; font-family: helvetica;">are</li>
            <li style="font-size: 11pt; font-family: helvetica;">you?</li>
        >>> 
        """
        text = text.strip()
        lines = text.split("\n")
        if text == "":
            return ""
        texted = []
        for line in lines:
            inptext = f"""<li style="font-size: 11pt; font-family: helvetica;">{line}</li>"""
            texted.append(inptext)
        text = "\n".join(texted)
        return text.strip()
def main():
    """Initalises the program
    """
    root = tk.Tk()

    UADescriptionEditor(root)
    root.mainloop()

if __name__ == '__main__':
    main()
 