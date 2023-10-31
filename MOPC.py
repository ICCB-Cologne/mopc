from shiny import App, render, ui, reactive
import pandas as pd
import pickle
import warnings
warnings.filterwarnings("ignore")
from pathlib import Path

app_ui = ui.page_fluid(
    ui.include_css('MOPC.css'),
    ui.div({'class':'centered-div'},
    ui.img(src="res/MOPC_logo.png", style='width: 100%;'),
    ui.br(),
    ui.br(),
    ui.p(),
    ui.h1("Welcome to MOP-C v0.3"),
    ui.p("MOP-C predicts risk of relapse in patients with CNS lymphoma. MOP-C includes clinical and molecular features assessed at baseline, after one cycle of therapy and at the end of induction therapy (Heger et al., Blood, 2023)."),
    #ui.p("This webtool allows users to predict risk of relapse in a patient with CNS lymphoma given that all required variables are available."),
    
    ui.strong("Important notes"),
    ui.p("""Please note that all variables are required for prediction. 
         For example, if 'ctDNA detected in plasma (at baseline)' is set to 'no', ctDNA levels are set to zero and PRD is set to negative both after 1 cycle of therapy and at the end of induction therapy.
         These values therefore influence the risk model and MOP-C cannot be used without the required variables."""),
    
    ui.strong("Disclaimer"),
    ui.p("""MOP-C is not validated in prospective clinical trials and does therefore not provide evidence to adjust, omit or intensify treatment of patients with CNS lymphoma. 
         MOP-C should only be used by healthcare professionals and is provided without any warranty. 
         All information contained in this system and produced by it are provided for educational purposes only. 
         In particular, any information found here or generated from the use of this system should not be used for the diagnosis or treatment of any health problem or disease. 
         MOP-C is not intended to replace any clinical judgement or guide individual patient care in any way."""),
    ui.hr(),

    ui.h1("MOP-C input variables"),
    ui.br(),
    ui.h2("Age (in years)"),
    ui.input_slider("AGE", "", 18,99,18),
    ui.br(),

    ui.h2("ECOG PS (Eastern Cooperative Oncology Group Performance Status)"),
    ui.input_slider("ECOG", "", 0,4,0),
    ui.br(),

    ui.h2("Deep brain structures involved (MRI at baseline)?"),
    ui.input_radio_buttons("DeepBrainStructures", "", {'0':"No",'1': "Yes"}),
    ui.br(),    
    
    ui.h2("Total protein in cerebrospinal fluid elevated (at baseline)?"),
    ui.input_radio_buttons("ProteinCerFluid", "", {'0':"No",'1': "Yes"}),
    ui.br(),    
    
    ui.h2("Serum LDH elevated (at baseline)?"),
    ui.input_radio_buttons("LDH", "", {'0':"No",'1': "Yes"}),
    ui.br(),
    
    ui.h2("ctDNA detected in plasma (at baseline)?"),
    ui.input_radio_buttons("ctDNAbaseline_radio_button","", {'0':"No",'1': "Yes"}),
    ui.panel_conditional("input.ctDNAbaseline_radio_button === '1'",
        ui.div({'class':'indent'},                         
            ui.h2("ctDNA level baseline in log hGE/mL plasma (haploid genome equivalents per mL plasma)"),
            ui.input_numeric("ctDNAbaseline","", value=2),
            ui.h2("PRD (peripheral residual disease) after 1 cycle of therapy detected?"),
            ui.input_radio_buttons("PRD_radio_input", "", {'0':"No",'1': "Yes"}),
            ui.panel_conditional("input.PRD_radio_input === '1'",
                ui.div({'class':'indent'},
                    ui.h2("Log10 change from baseline"),
                    ui.input_slider("PRD_input_slider","",-5,1,-5, step=0.1))),
            ui.br(),
            ui.h2("PRD (peripheral residual disease) at the end of induction therapy detected?"),
            ui.input_radio_buttons("PRD_radio_end", "", {'0':"No",'1': "Yes"}),
            ui.panel_conditional("input.PRD_radio_end === '1'",
                ui.div({'class':'indent'},                                 
                    ui.h2("Log10 change from baseline"), 
                    ui.input_slider("PRD_end_slider","",-5,1,-5, step=0.1))))),
    ui.br(),

    ui.h2("Complete remission achieved (MRI at the end of induction therapy)?"),
    ui.input_radio_buttons("CompleteRemission", "", {'0':"No",'1': "Yes"}),
    ui.br(),    
    ui.p(ui.input_action_button("button", "Run MOP-C",class_="btn-primary", onclick='document.getElementById("div_results").scrollIntoView();')),
    ui.hr(),
    ui.div({'id':'div_results'},
        ui.output_ui("out_header"),
        ui.output_text_verbatim("out_results")),
    ui.hr(),
    ui.img(src="res/ICCB_logo.png", width="200px", align='left', style='margin-right: 20px;'),
    ui.div(
    ui.p("""MOP-C Shiny app implementation by Teodora Bucaciuc and Roland Schwarz, (c) """, ui.a("Schwarzlab", href="http://schwarzlab.de", target="_blank"), 
         """ 2023, Institute for Computational Cancer Biology (ICCB, """, ui.a("https://iccb-cologne.org", href="https://iccb-cologne.org"), """), Center for Integrated Oncology (CIO), 
         Cancer Research Center Cologne Essen (CCCE), Faculty of Medicine and University Hospital Cologne, University of Cologne, Germany. """, 
         ui.tags.br(), ui.tags.br(), ui.tags.u("Code available"), " on ", ui.a("https://github.com/schwarzlab/MOP-C", href="https://github.com/schwarzlab/MOP-C"), 
         " under MIT license. """, ui.tags.u("Technical contact:"), " roland.schwarz@iccb-cologne.org."), 
    ui.p("Predictive model and clinical interpretation by Jan-Michel Heger and Sven Borchman, ", ui.a("Borchmann Lab", href="https://sven-borchmann.owlstown.net", target="_blank"), ", Department of Internal Medicine I, Center for Integrated Oncology (CIO), University Hospital Cologne, Germany. ", ui.tags.u("Contact:"), " sven.borchmann@uk-koeln.de."),
    ui.p(ui.tags.u("Publication: "), "Heger M et al. ", ui.em("Entirely noninvasive outcome prediction in central nervous system lymphomas using circulating tumor DNA. "),"Blood 2023."), style='text-align: left;')
    )
)

my_dir=Path(__file__).parent / ""
value_ML_min=-3.6737
with open('res/Model_flaml_pcnsl_total.pkl', 'rb') as mypickle:
    my_model = pickle.load(mypickle)

def prediction_output(age, ecog, deepbrainstruc, proteincerfluid, ldh, ctdna, prd_input_slider, prd_end_slider, completeremission):
    patient_features=[age, ecog, deepbrainstruc, proteincerfluid, ldh, ctdna, prd_input_slider, prd_end_slider, completeremission]   
    patient_features_df=pd.DataFrame([patient_features], columns=['age', 'ECOG', 'deep_brain_structure', 'CSF_protein_measured', 'LDH_elevated', 'ctDNA', 'log_PRD_mid', 'log_PRD_post', 'CR_reached'])
    predict_new=my_model.predict(patient_features_df)
    prob= my_model.predict_proba(patient_features_df)[0][1]
        
    if 0<=prob*100<=16.5:
        statement="low risk"
    elif 16.5<prob*100<=50:
        statement="intermediate risk"
    elif prob*100>50:
        statement="high risk"
    else:
        statement="error"
    return f"Predicted score: "+ str(round(float(prob)*100, 2))+"%"+"\nRisk group: "+ statement


def server(input, output, session):
    @output
    @render.ui
    @reactive.event(input.button)
    def out_header():
        return ui.h1("MOP-C prediction results")

    @output
    @render.text
    @reactive.event(input.button)
    def out_results():
        if input.ctDNAbaseline_radio_button()=='0':
            input.ctDNAbaseline() == 0
            #ui.update_radio_buttons("PRD_radio_input", label="", choices=[value_ML_min])
            #ui.update_radio_buttons("PRD_radio_end", label="", choices=[value_ML_min])
            input.PRD_input_slider()==value_ML_min
            input.PRD_end_slider()==value_ML_min
            result = prediction_output(input.AGE(), input.ECOG(), input.DeepBrainStructures(), input.ProteinCerFluid(),input.LDH(), input.ctDNAbaseline(), input.PRD_input_slider(), input.PRD_end_slider(), input.CompleteRemission())

        elif input.ctDNAbaseline_radio_button()== '1':
            if input.PRD_radio_input()=='0':
                #ui.update_radio_buttons("PRD_radio_input", label="", choices=[value_ML_min])
                input.PRD_input_slider()==value_ML_min
                result = prediction_output(input.AGE(), input.ECOG(), input.DeepBrainStructures(), input.ProteinCerFluid(),input.LDH(), input.ctDNAbaseline(), input.PRD_input_slider(), input.PRD_end_slider(), input.CompleteRemission())
            elif input.PRD_radio_end()=='0':
                #ui.update_radio_buttons("PRD_radio_end", label="", choices=[value_ML_min])
                input.PRD_end_slider()==value_ML_min
                result = prediction_output(input.AGE(), input.ECOG(), input.DeepBrainStructures(), input.ProteinCerFluid(),input.LDH(), input.ctDNAbaseline(), input.PRD_input_slider(), input.PRD_end_slider(), input.CompleteRemission())
            elif input.PRD_radio_end()=='0' and input.PRD_radio_end()=='0':
                #ui.update_radio_buttons("PRD_radio_input", label="", choices=[value_ML_min])
                #ui.update_radio_buttons("PRD_radio_end", label="", choices=[value_ML_min])
                input.PRD_input_slider()==value_ML_min
                input.PRD_end_slider()==value_ML_min
                result = prediction_output(input.AGE(), input.ECOG(), input.DeepBrainStructures(), input.ProteinCerFluid(),input.LDH(), input.ctDNAbaseline(), input.PRD_input_slider(), input.PRD_end_slider(), input.CompleteRemission())
            else:
                result = prediction_output(input.AGE(), input.ECOG(), input.DeepBrainStructures(), input.ProteinCerFluid(),input.LDH(), input.ctDNAbaseline(), input.PRD_input_slider(), input.PRD_end_slider(), input.CompleteRemission())

        return result
    


app = App(app_ui, server, static_assets=my_dir)

