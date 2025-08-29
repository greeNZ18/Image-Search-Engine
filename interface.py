import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from backend import download_image, scrape_images

def create_interface():
    # Create the main window
    root = tk.Tk()
    root.title("Image Search Engine")
    root.geometry("1000x700")
    root.configure(bg="#2C3E50")  # Modern dark background
    root.resizable(True, True)

    # Styling
    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 12), foreground="white", background="#2C3E50")
    style.configure("TButton", font=("Helvetica", 12, "bold"), background="#27AE60", foreground="white")
    style.map("TButton", background=[("active", "#2ECC71")])  # Light green on hover
    style.configure("TEntry", font=("Helvetica", 12), fieldbackground="#ECF0F1", foreground="black")

    # Add a title
    title_label = tk.Label(
        root,
        text="🌟 Welcome to Image Search Engine 🌟",
        font=("Helvetica", 20, "bold"),
        bg="#2C3E50",
        fg="#ECF0F1"
    )
    title_label.pack(pady=20)

    # Input section
    input_frame = tk.Frame(root, bg="#34495E", bd=5, relief=tk.RIDGE)
    input_frame.pack(pady=10, padx=20, fill=tk.X)

    search_var = tk.StringVar()
    search_label = tk.Label(
        input_frame,
        text="🔍 Enter search term:",
        font=("Helvetica", 14),
        bg="#34495E",
        fg="#ECF0F1"
    )
    search_label.pack(side="left", padx=10)

    search_entry = ttk.Entry(input_frame, textvariable=search_var, width=50)
    search_entry.pack(side="left", padx=10)

    def animate_button(e):
        search_button.configure(style="Hover.TButton")

    def reset_button(e):
        search_button.configure(style="TButton")

    # Custom hover style for the search button
    style.configure("Hover.TButton", font=("Helvetica", 12, "bold"), background="#2ECC71", foreground="white")

    # Search button
    search_button = ttk.Button(input_frame, text="Search", command=lambda: on_search())
    search_button.pack(side="left", padx=10)
    search_button.bind("<Enter>", animate_button)
    search_button.bind("<Leave>", reset_button)

    # Results section
    results_frame = tk.Frame(root, bg="#34495E", bd=5, relief=tk.RIDGE)
    results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Scrollable canvas for results
    canvas = tk.Canvas(results_frame, bg="#34495E", highlightthickness=0)
    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#34495E")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Display results
    def display_results(images):
        # Clear previous results
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        if not images:
            tk.Label(
                scrollable_frame,
                text="🚫 No results found!",
                font=("Helvetica", 14, "italic"),
                fg="red",
                bg="#34495E"
            ).pack(pady=20)
            return

        for img_info in images:
            try:
                # Download the image
                img_data = download_image(img_info["src"])
                if img_data:
                    img_data.thumbnail((300, 300))  # Resize the image
                    img_tk = ImageTk.PhotoImage(img_data)

                    # Display the image and its details
                    result_frame = tk.Frame(scrollable_frame, bg="#2C3E50", bd=2, relief=tk.RAISED)
                    result_frame.pack(pady=10, padx=10, fill="x")

                    image_label = tk.Label(result_frame, image=img_tk, bg="#2C3E50")
                    image_label.image = img_tk  # Keep a reference
                    image_label.pack(side="left", padx=10, pady=10)

                    details_label = tk.Label(
                        result_frame,
                        text=f"Alt: {img_info['alt']}\nNearby Text: {img_info['nearby_text']}\nSource: {img_info['source']}",
                        font=("Helvetica", 12),
                        fg="#ECF0F1",
                        bg="#2C3E50",
                        justify="left",
                        anchor="w"
                    )
                    details_label.pack(side="left", padx=10)
            except Exception as e:
                tk.Label(
                    scrollable_frame,
                    text=f"Error displaying image: {e}",
                    font=("Helvetica", 12, "italic"),
                    fg="red",
                    bg="#34495E"
                ).pack(pady=5)

    # Search action
    def on_search():
        query = search_var.get()
        if query:
            results = scrape_images(query)  # Call backend function
            if results:
                display_results(results)
            else:
                messagebox.showinfo("No Results", "No images found matching your query.")
        else:
            messagebox.showerror("Input Error", "Please enter a search term.")

    # Footer
    footer_label = tk.Label(
        root,
        text="💡 Tip: Use '+' for OR logic (e.g., 'cat+dog')",
        font=("Helvetica", 10, "italic"),
        bg="#2C3E50",
        fg="#BDC3C7"
    )
    footer_label.pack(side="bottom", pady=10)

    # Run the app
    root.mainloop()
