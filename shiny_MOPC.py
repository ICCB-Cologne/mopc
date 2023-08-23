from shiny import App, render, ui, reactive
import pandas as pd
import pickle
import warnings
warnings.filterwarnings("ignore")
from pathlib import Path



app_ui = ui.page_fluid(

    
    ui.panel_title("MOP-C"),
    ui.img(src="Logo_large.png"),


    ui.h4("Add age (in years)"),
    ui.input_slider("AGE", "", 18,99,18),
    

    ui.h4("Add ECOG PS (Eastern Cooperative Oncology Group Performance Status)"),
    ui.input_slider("ECOG", "", 0,4,0),
    

    ui.h4("Are deep brain structures involved (MRI)?"),
    ui.input_radio_buttons("DeepBrainStrunctures", "Select", {'0':"NO",'1': "YES"}),
    

    ui.h4("Is the total protein in cerebrospinal fluid elevated?"),
    ui.input_radio_buttons("ProteinCerFluid", "Select", {'0':"NO",'1': "YES"}),
    
    
    ui.h4("Is serum LDH (at baseline) elevated?"),
    ui.input_radio_buttons("LDH", "Select", {'0':"NO",'1': "YES"}),
    

    ui.h4("Peripheral ctDNA at baseline detected?"),
    ui.input_radio_buttons("ctDNAbaseline_radio_button","Select", {'0':"NO",'1': "YES"}),
    ui.panel_conditional("input.ctDNAbaseline_radio_button === '1'",
                         ui.h4("Add ctDNA level baseline in log hGE/mL plasma (haploid genome equivalents per mL plasma)"),
                         ui.input_numeric("ctDNAbaseline","", value=2),
                         ui.h4("PRD (peripheral residual disease) after 1 cycle of therapy detected?"),
    ui.input_radio_buttons("PRD_radio_input","Select", {'0':"NO",'1': "YES"}),
    ui.panel_conditional("input.PRD_radio_input === '1'",
                         ui.h4("Add log10 change from baseline"), ui.input_slider("PRD_input_slider","",-5,1,-5, step=0.1)),
    

    ui.h4("PRD (peripheral residual disease) at the end of induction therapy detected?"),
    ui.input_radio_buttons("PRD_radio_end","Select", {'0':"NO",'1': "YES"}),
    ui.panel_conditional("input.PRD_radio_end === '1'",
                         ui.h4("Add log10 change from baseline"), ui.input_slider("PRD_end_slider","",-5,1,-5, step=0.1))),

    ui.h4("Was complete remission (MRI) achieved at the end of induction therapy?"),
    ui.input_radio_buttons("CompleteRemission", "Select", {'0':"NO",'1': "YES"}),
    

    ui.p(ui.input_action_button("button", "Classify patient", class_="btn-primary")),
    ui.tags.br(),
    ui.output_text_verbatim("txt"),
    
)

my_dir=Path(__file__).parent / ""
value_ML_min=-3.6737
with open('Model_flaml_pcnsl_total.pkl', 'rb') as mypickle:
    my_model = pickle.load(mypickle)

def prediction_output(age, ecog, deepbrainstruc, proteincerfluid, ldh, ctdna, prd_input_slider, prd_end_slider, completeremission):
    patient_features=[age, ecog, deepbrainstruc, proteincerfluid, ldh, ctdna, prd_input_slider, prd_end_slider, completeremission]   
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


def server(input, output, session):
    @output
    @render.text
    @reactive.event(input.button)


    def txt():
        if input.ctDNAbaseline_radio_button()=='0':
            input.ctDNAbaseline() == 0
            #ui.update_radio_buttons("PRD_radio_input", label="", choices=[value_ML_min])
            #ui.update_radio_buttons("PRD_radio_end", label="", choices=[value_ML_min])
            input.PRD_input_slider()==value_ML_min
            input.PRD_end_slider()==value_ML_min
            return prediction_output(input.AGE(), input.ECOG(), input.DeepBrainStrunctures(), input.ProteinCerFluid(),input.LDH(), input.ctDNAbaseline(), input.PRD_input_slider(), input.PRD_end_slider(), input.CompleteRemission())

        elif input.ctDNAbaseline_radio_button()== '1':
            if input.PRD_radio_input()=='0':
                #ui.update_radio_buttons("PRD_radio_input", label="", choices=[value_ML_min])
                input.PRD_input_slider()==value_ML_min
                return prediction_output(input.AGE(), input.ECOG(), input.DeepBrainStrunctures(), input.ProteinCerFluid(),input.LDH(), input.ctDNAbaseline(), input.PRD_input_slider(), input.PRD_end_slider(), input.CompleteRemission())
            elif input.PRD_radio_end()=='0':
                #ui.update_radio_buttons("PRD_radio_end", label="", choices=[value_ML_min])
                input.PRD_end_slider()==value_ML_min
                return prediction_output(input.AGE(), input.ECOG(), input.DeepBrainStrunctures(), input.ProteinCerFluid(),input.LDH(), input.ctDNAbaseline(), input.PRD_input_slider(), input.PRD_end_slider(), input.CompleteRemission())
            elif input.PRD_radio_end()=='0' and input.PRD_radio_end()=='0':
                #ui.update_radio_buttons("PRD_radio_input", label="", choices=[value_ML_min])
                #ui.update_radio_buttons("PRD_radio_end", label="", choices=[value_ML_min])
                input.PRD_input_slider()==value_ML_min
                input.PRD_end_slider()==value_ML_min
                return prediction_output(input.AGE(), input.ECOG(), input.DeepBrainStrunctures(), input.ProteinCerFluid(),input.LDH(), input.ctDNAbaseline(), input.PRD_input_slider(), input.PRD_end_slider(), input.CompleteRemission())
            else:
                return prediction_output(input.AGE(), input.ECOG(), input.DeepBrainStrunctures(), input.ProteinCerFluid(),input.LDH(), input.ctDNAbaseline(), input.PRD_input_slider(), input.PRD_end_slider(), input.CompleteRemission())
        
           
   

app = App(app_ui, server, static_assets=my_dir)

