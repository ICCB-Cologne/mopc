from shiny import App, render, ui, reactive
import pandas as pd
import pickle
import warnings
warnings.filterwarnings("ignore")


app_ui = ui.page_fluid(

    ui.panel_title("MOP-C"),

    ui.h4("Add age (in years)"),
    ui.input_numeric("AGE", "Age input", value=0),
    

    ui.h4("Add ECOG PS (Eastern Cooperative Oncology Group Performance Status)"),
    ui.input_numeric("ECOG", "ECOG input", value=0),
    

    ui.h4("Are deep brain structures involved (MRI)?"),
    ui.input_radio_buttons("DeepBrainStrunctures", "Select", {'1': "YES", '0':"NO"}),
    

    ui.h4("Is the total protein in cerebrospinal fluid elevated?"),
    ui.input_radio_buttons("ProteinCerFluid", "Select", {'1': "YES", '0':"NO"}),
    
    
    ui.h4("Is serum LDH (at baseline) elevated ?"),
    ui.input_radio_buttons("LDH", "Select", {'1': "YES", '0':"NO"}),
    

    ui.h4("Add ctDNA level (at baseline) in log10 hGE/mL plasma (haploid genome equivalents per mL plasma)"),
    ui.input_numeric("ctDNAbaseline", "ctDNA at baseline", value=0),
    

    ui.h4("Add PRD (peripheral residual disease) after 1 cycle of therapy (log10 reduction from baseline)"),
    ui.input_numeric("PRD_input", "PRD", value=0),
    

    ui.h4("Add PRD (peripheral residual disease) at the end of induction therapy"),
    ui.input_numeric("PRD_completion", "PRD", value=0),

    ui.h4("Complete remission (MRI) achieved at the end of induction therapy"),
    ui.input_radio_buttons("CompleteRemission", "Select", {'1': "YES", '0':"NO"}),
    

    ui.p(ui.input_action_button("button", "Classify patient", class_="btn-primary")),
    ui.tags.br(),
    ui.output_text_verbatim("txt"),
    
)


with open('Model_flaml_pcnsl_total.pkl', 'rb') as mypickle:
    my_model = pickle.load(mypickle)

def server(input, output, session):
    @output
    @render.text
    @reactive.event(input.button)


    def txt():
        
        
        patient_features=[input.AGE(), input.ECOG(), input.DeepBrainStrunctures(), input.ProteinCerFluid(),input.LDH(), input.ctDNAbaseline(), input.PRD_input(), input.PRD_completion(), input.CompleteRemission()]
       
        patient_features_df=pd.DataFrame([patient_features], columns=['age', 'ECOG', 'deep_brain_structure', 'CSF_protein_measured', 'LDH_elevated', 'ctDNA', 'log_PRD_mid', 'log_PRD_post', 'CR_reached'])
        
        
        predict_new=my_model.predict(patient_features_df)
        prob= my_model.predict_proba(patient_features_df)[0][1]
        
        if 0<=prob*100<=16.5:
            statememnt="low risk"
        elif 16.5<prob*100<=50:
            statememnt="intermediate risk"
        elif prob*100>50:
            statememnt="high risk"         

        
        return f"Predicted score: "+ str(round(float(prob)*100, 2))+"%"+"\nRisk group: "+ statememnt
   

app = App(app_ui, server)

