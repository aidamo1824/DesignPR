import tkinter as tk
from tkinter import ttk, messagebox

class DesignPR:
    def __init__(self, root):
        self.root = root
        self.root.title("PCR Primer Design Tool")
        self.create_frames()
    
    def create_frames(self): 
        
        self.create_purpose_frame()
        self.create_sequence_frame()
        self.create_method_frame()
        self.create_result_frame()
        self.create_action_buttons()
    
    def create_purpose_frame(self):
        
        purpose_frame = ttk.LabelFrame(root, text="Primers Purpose")
        purpose_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.purpose_user = tk.StringVar(value="Insertion")
        purposes = ["Insertion", "Deletion", "Point Mutation", "2-Fragment Assembly"]
        for idx, purpose in enumerate(purposes):
            ttk.Radiobutton(purpose_frame, text=purpose, value=purpose, variable=self.purpose_user, command=self.update_sequence_fields).grid(row=0, column=idx, padx=5, pady=5)
    
    def create_sequence_frame(self):
    
        self.seq_frame = ttk.Frame(root)
        self.seq_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.update_sequence_fields()


    def create_method_frame(self): 
        
        method_frame = ttk.LabelFrame(root, text="Cloning Method")
        method_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.method_var = tk.StringVar(value="IVA")
        self.method_list = ["IVA"]
        self.method_menu = ttk.OptionMenu(method_frame, self.method_var, "IVA", *self.method_list)
        self.method_menu.grid(row=0, column=0, padx=5, pady=5)
        
        
    def create_result_frame(self):
        
        result_frame = ttk.LabelFrame(root, text="Designed Primers")
        result_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.result_text = tk.Text(result_frame, height=10, width=60, state="disabled")
        self.result_text.grid(row=0, column=0, padx=5, pady=5)

    def create_action_buttons(self):
        button_frame = ttk.Frame(root)
        button_frame.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        ttk.Button(button_frame, text="Design Primers", command=self.design_primers).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_all).grid(row=0, column=1, padx=5, pady=5)
        


    def update_sequence_fields(self):
        # Clear existing sequence fields
        for widget in self.seq_frame.winfo_children():
            widget.destroy()

        # Update sequence fields based on selected purpose
        purpose = self.purpose_user.get()
        first_frame_title = "DNA Sequence"
        second_frame_title = "Insert Sequence"

        if purpose == "Deletion":
            second_frame_title = "Sequence to Delete"  
        elif purpose == "Point Mutation":
            second_frame_title = "Mutation [original_codon;new_codon]"
        elif purpose == "2-Fragment Assembly": 
            first_frame_title = "Backbone Sequence"
        
        
        #Sequence frame 1
        seq_frame = ttk.LabelFrame(self.seq_frame, text=first_frame_title)
        seq_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        ttk.Label(seq_frame, text="Sequence:").grid(row=0, column=0, padx=5, pady=5)
        self.seq_entry_1 = tk.Text(seq_frame, height=5, width=50)
        self.seq_entry_1.grid(row=0, column=1, padx=5, pady=5)
            
        #Sequence frame 2
        seq_frame = ttk.LabelFrame(self.seq_frame, text=second_frame_title)
        seq_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        ttk.Label(seq_frame, text="Sequence:").grid(row=0, column=0, padx=5, pady=5)
        self.seq_entry_2 = tk.Text(seq_frame, height=5, width=50)
        self.seq_entry_2.grid(row=0, column=1, padx=5, pady=5)
       

    def checkSEQ(self): 
        seq_1 = self.seq_entry_1.get("1.0", tk.END).strip().upper()
        seq_2 = self.seq_entry_2.get("1.0", tk.END).strip().upper()
        seq_entries = [seq_1, seq_2]
        for seq in seq_entries: 
            if not seq:   
                messagebox.showerror("Input Error", "Please enter a valid DNA sequence.")
                return
            
            allowed_char = ["A", "T", "C", "G", ";"]
            for char in seq: 
                if char not in allowed_char: 
                    messagebox.showerror("Input Error", "Invalid characters found in sequence.")
                    return   
        
        return seq_entries    
    
    def reverse_complement(self, sequence):
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        return ''.join(complement[base] for base in reversed(sequence))
    
    
    def design_primers(self):
        primer_purpose = self.purpose_user.get()
        seq_entries = self.checkSEQ()
        
        default_length_homologous = 15
        default_length_overlap = 12
        
        
        if(primer_purpose == "Insertion"):
            Backbone_seq = seq_entries[0]
            Ins_seq = seq_entries[1]
            if len(Ins_seq) > 15: 
                messagebox.showerror("Input Error", "Please use 2-Fragment Assembly for inserts longer than 15-bps.")
                return
                

            fwd_homologous = Backbone_seq[:15]
            rev_homologous = self.reverse_complement(Backbone_seq[-15:]+Ins_seq)
            primers = {
                "forward": {Ins_seq + fwd_homologous}, 
                "reverse": {rev_homologous}
            }
        
        elif(primer_purpose == "Deletion"): 
            DNA_seq = seq_entries[0]
            delete_seq = seq_entries[1]
            
            fwd_start = len(delete_seq)
            fwd_end = 15+fwd_start
            print(fwd_start)
            
            if delete_seq in DNA_seq: 
                fwd_homologous = DNA_seq[fwd_start:fwd_end]
                rev_homologous = self.reverse_complement(DNA_seq[-15:]+ DNA_seq[fwd_start:fwd_end])
                
                primers = {
                    "forward": {DNA_seq[-15:] + fwd_homologous},
                    "reverse": {rev_homologous}
                }
            else: 
                messagebox.showerror("Input Error", "Sequence to delete not found in DNA sequence.")
                
        elif(primer_purpose == "2-Fragment Assembly"):
            BB_seq = seq_entries[0]
            INS_seq = seq_entries[1]
            
            fwd_BB_homologous = BB_seq[:15]
            fwd_BB_overlap = INS_seq[-12:]
            
            rev_BB_homologous = BB_seq[-15:]
            rev_BB_overlap = INS_seq[:12]
            
            fwd_BB = fwd_BB_overlap + fwd_BB_homologous
            rev_BB = self.reverse_complement(rev_BB_homologous + rev_BB_overlap)
            
            
            fwd_INS_homologous = INS_seq[:15]
            fwd_INS_overlap = BB_seq[-12:]
            
            rev_INS_homologous = INS_seq[-15:]
            rev_INS_overlap = BB_seq[:12]
            
            fwd_INS = fwd_INS_overlap + fwd_INS_homologous
            rev_INS = self.reverse_complement(rev_INS_homologous + rev_INS_overlap)
            
            
            primers = {
                "BB_forward": {fwd_BB},
                "BB_reverse": {rev_BB},
                
                "INS_forward": {fwd_INS},
                "INS_reverse": {rev_INS}
        
            }
        
        #for point mutations 
        else: 
            DNA_seq = seq_entries[0]
            original_codon, new_codon = seq_entries[1].split(";")
            
            fwd_point_homologous = DNA_seq[:15]
            fwd_point_overlap = DNA_seq[-12:]
            
            rev_point_homologous = DNA_seq[-15:] 
            rev_point_overlap = DNA_seq[:12]
            
            fwd_point_primer = fwd_point_overlap + new_codon + fwd_point_homologous
            rev_point_primer = self.reverse_complement(rev_point_homologous + rev_point_overlap)
            
            primers = {
                "mutation" : {original_codon + "-->" + new_codon},
                "forward": {fwd_point_primer},
                "reverse": {rev_point_primer}
            }



        self.display_primers(primers)
     
    def display_primers(self, primers):
        
        print(f"Displaying primers: {primers}")
        primer_purpose = self.purpose_user.get()
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        if primer_purpose == "2-Fragment Assembly":
            self.result_text.insert(tk.END, f"Backbone Forward Primer: {primers['BB_forward']}\n")
            self.result_text.insert(tk.END, f"Backbone Reverse Primer: {primers['BB_reverse']}\n")
            self.result_text.insert(tk.END, f"Insert Forward Primer: {primers['INS_forward']}\n")
            self.result_text.insert(tk.END, f"Insert Reverse Primer: {primers['INS_reverse']}\n")
       
        elif primer_purpose == "Point Mutation":
            self.result_text.insert(tk.END, f"Point Mutation: {primers['mutation']}\n")
            self.result_text.insert(tk.END, f"Forward Primer: {primers['forward']}\n")
            self.result_text.insert(tk.END, f"Reverse Primer: {primers['reverse']}\n")
            
        elif 'forward' in primers and 'reverse' in primers:
            self.result_text.insert(tk.END, f"Forward Primer: {primers['forward']}\n")
            self.result_text.insert(tk.END, f"Reverse Primer: {primers['reverse']}\n")
        else:
            print("Error: Missing primer data.")
        self.result_text.config(state="disabled")


    def clear_all(self):
        self.seq_entry_1.delete("1.0", tk.END)
        self.seq_entry_2.delete("1.0", tk.END)
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")


def main():
    root = tk.Tk()
    app = DesignPR(root)
    root.mainloop()

if __name__ == "__main__":
    main()
