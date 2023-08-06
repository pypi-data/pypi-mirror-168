#!/usr/bin/env python
#---------------------------------------------------------------------------
# Copyright 2021 Takafumi Ogawa
# Licensed under the Apache License, Version2.0.
#---------------------------------------------------------------------------
# pydecs-io module
#---------------------------------------------------------------------------
import os,sys
import shutil
import copy
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import toml

from pydecs.common import product_local

def parse_composition_list(comp_in):
    comp1=[]
    ic0=0
    for ic1,c1 in enumerate(comp_in):
        if ic1!=0 and c1.isupper():
            comp1.append(comp_in[ic0:ic1])
            ic0=ic1
    comp1.append(comp_in[ic0:])
    atomList=[]
    for c1 in comp1:
        elem1=""
        num1=""
        for c2 in c1:
            if c2.isdigit():
                num1+=c2
            else:
                elem1+=c2
        if len(num1)==0:
            num1="1"
        atomList.append((elem1,int(num1)))
    return atomList


class InputParamsToml:

    def __init__(self,filename_in="inpydecs.toml"):
        if not os.path.exists(filename_in):
            print(" ERROR: file not-found: "+filename_in)
            sys.exit()
        print(" Reading input-file: "+filename_in)
        try:
            self.input_parameters=toml.load(filename_in)
        except Exception as e:
            print(" ERROR: Check TOML-format in the input file")
            print("  => "+str(e))
            sys.exit()
        self.input_paths=["./"]
        self.outfiles_header="outpydecs"
        if "io" in self.input_parameters.keys():
            p1=self.input_parameters["io"]
            if "input_paths" in p1.keys():
                self.input_paths=p1["input_paths"]
            if "input_paths" in p1.keys():
                self.outfiles_header=p1["outfiles_header"]
        for i1,p1 in enumerate(self.input_paths):
            if p1[-1]!="/":
                self.input_paths[i1]=p1+"/"
        str1=f"  input_paths = [\""
        for p1 in self.input_paths:
            str1=str1+f"{p1}\", \""
        print(str1[:-3]+"]")
        print("  outfiles_header = "+self.outfiles_header)
        print("-"*100)

    def get_input_parameters(self):
        return self.input_parameters

    def get_input_paths(self):
        return self.input_paths
    
    def get_root_outfiles(self):
        return self.outfiles_header


def plot_Edef_eFermi(filename_in,root_outfiles,plot_params_in={}):
    if not "format" in plot_params_in.keys():
        plot_params_in["format"]=["png"]
    if not "dpi" in plot_params_in.keys():
        plot_params_in["dpi"]=100
    if not "figsize_x_cm" in plot_params_in.keys():
        plot_params_in["figsize_x_cm"]=9.0
    if not "figsize_y_cm" in plot_params_in.keys():
        plot_params_in["figsize_y_cm"]=8.0
    plot_params_in["figsize_x_inch"]=plot_params_in["figsize_x_cm"]/2.54
    plot_params_in["figsize_y_inch"]=plot_params_in["figsize_y_cm"]/2.54
    if not "label_size" in plot_params_in.keys():
        plot_params_in["label_size"]=10
    if not "ticks_size" in plot_params_in.keys():
        plot_params_in["ticks_size"]=8
    if not "ticks_pad" in plot_params_in.keys():
        plot_params_in["ticks_pad"]=4.0
    if not "replace_V_for_Vac" in plot_params_in.keys():
        plot_params_in["replace_V_for_Vac"]=True
    if not "Edef_x_lower_limit" in plot_params_in.keys():
        plot_params_in["Edef_x_lower_limit"]=0.0
    if not "Edef_x_upper_limit" in plot_params_in.keys():
        plot_params_in["Edef_x_upper_limit"]="BAND_GAP"
    if not "Edef_xlabel" in plot_params_in.keys():
        plot_params_in["Edef_xlabel"]=r"$\varepsilon_\mathrm{F}-\varepsilon_\mathrm{VBM}\ \mathrm{[eV]}$"
    if not "Edef_y_lower_limit" in plot_params_in.keys():
        plot_params_in["Edef_y_lower_limit"]=0.0
    if not "Edef_y_upper_limit" in plot_params_in.keys():
        plot_params_in["Edef_y_upper_limit"]=3.0
    if not "Edef_xtick_labels" in plot_params_in.keys():
        plot_params_in["Edef_xtick_labels"]="NONE"
    if not "Edef_ytick_labels" in plot_params_in.keys():
        plot_params_in["Edef_ytick_labels"]="NONE"
    if not "Edef_ylabel" in plot_params_in.keys():
        plot_params_in["Edef_ylabel"]=r"$\mathrm{Defect\ formation\ energy\ [eV]}$"
    if not "Edef_zero_line" in plot_params_in.keys():
        plot_params_in["Edef_zero_line"]=True
    if not "Edef_bands_fill" in plot_params_in.keys():
        plot_params_in["Edef_bands_fill"]=True
    if not os.path.exists(filename_in):
        print(" ERROR: file not-found: "+filename_in)
        sys.exit()
    fin=open(filename_in).readlines()
    for l1 in fin:
        if "Fermi_level" in l1:
            labels=l1.split(",")
            num_data=len(labels)
        if l1.strip()[0]!="#":
            continue
        if "Egap" in l1:
            Egap=float(l1.split(",")[0].split("=")[1].strip())
    if plot_params_in["Edef_x_upper_limit"]=="BAND_GAP":
        plot_params_in["Edef_x_upper_limit"]=Egap
    eFermi_list=[]
    charge_list=[]
    defects_list=[]
    for lab1 in labels[2:]:
        dict1={"label":lab1,"defect_energy":[]}
        dict1["defect_fineid"]=lab1.split("(")[1].split(")")[0]
        dict1["charge"]=lab1.split("{")[1].split("}")[0]
        if float(dict1["charge"])>0:
            dict1["charge"]="+"+dict1["charge"]
        def_label1=lab1.split("[")[1].split("]")[0]
        dict1["label_withoutQ"]=def_label1
        if "+" in def_label1:
            def_label3="["
            for def_label1sep in def_label1.split("+"):
                def_label2=def_label1sep.split("_")
                if def_label2[0]=="Vac" and plot_params_in["replace_V_for_Vac"]:
                    def_label2[0]="V"
                def_label3+="\mathrm{"+def_label2[0]+"}_\mathrm{"+def_label2[1]+"}+"
            def_label3=def_label3[:-1]+"]"
        else:
            def_label2=def_label1.split("_")
            if def_label2[0]=="Vac" and plot_params_in["replace_V_for_Vac"]:
                def_label2[0]="V"
            def_label3="\mathrm{"+def_label2[0]+"}_\mathrm{"+def_label2[1]+"}"
        dict1["label_for_legend"]="$"+def_label3+"$"
        def_label4=def_label3+"^{"+dict1["charge"]+"}"
        dict1["label_for_legend_withQ"]="$"+def_label4+"$"
        if dict1["defect_fineid"]=="0":
            def_label5=def_label4
        else:
            def_label5=def_label4+"("+dict1["defect_fineid"]+")"
        dict1["label_for_legend_withQ_withID"]="$"+def_label5+"$"
        defects_list.append(dict1)
    for l1 in fin:
        if l1.strip()[0]=="#":
            continue
        l2=l1.split(",")
        mode2=""
        if l2[0]=="line_color":
            mode2=l2[0]
        elif l2[0]=="line_style":
            mode2=l2[0]
        elif l2[0]=="line_width":
            mode2=l2[0]
        elif l2[0]=="Fermi_level":
            mode2="label"
        else:
            mode2="data"
        if mode2=="data":
            eFermi_list.append(float(l2[0]))
            charge_list.append(float(l2[1]))
        for i3,v3 in enumerate(l2[2:]):
            if mode2=="line_color":
                defects_list[i3]["line_color"]=v3.strip()
            elif mode2=="line_style":
                defects_list[i3]["line_style"]=v3.strip()
            elif mode2=="line_width":
                defects_list[i3]["line_width"]=v3.strip()
            elif mode2=="data":
                defects_list[i3]["defect_energy"].append(float(v3))
    #### Plotting Total_charge
    plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
    plt.tick_params(axis="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
    plt.plot(eFermi_list,charge_list,"k-",linewidth=2.0)
    plt.yscale("symlog",linthresh=10**-20)
    plt.xlim([plot_params_in["Edef_x_lower_limit"],plot_params_in["Edef_x_upper_limit"]])
    plt.ylim([min(charge_list)*1.1,max(charge_list)*1.1])
    plt.axhline(0.0,color="k",ls=":",lw=1.0)
    plt.ylabel(r"$\mathrm{Total\ charge\ [e/cell]}$",size=plot_params_in["label_size"])
    plt.xlabel(r"$\varepsilon_\mathrm{F}-\varepsilon_\mathrm{VBM}\ \mathrm{[eV]}$",size=plot_params_in["label_size"])
    if plot_params_in["Edef_xtick_labels"]!="NONE":
        plt.xticks(plot_params_in["Edef_xtick_labels"])
    for f1 in plot_params_in["format"]:
        plt.savefig(root_outfiles+"_Edef_Qtot."+f1,dpi=plot_params_in["dpi"])
    plt.close()
    
    eFermi_balanced = 1e10
    charge_balanced = 1e10
    for ie1,e1 in enumerate(eFermi_list):
        chg1=np.fabs(charge_list[ie1])
        if chg1<charge_balanced:
            charge_balanced=chg1
            eFermi_balanced=e1
    #### Determining plot-range
    lowestEf_line=[]
    for i1,e1 in enumerate(eFermi_list):
        emin=1e20
        for d2 in defects_list:
            e2=d2["defect_energy"][i1]
            if e1<emin:
                emin=e1
        lowestEf_line.append(emin)
    max_lowestEf=max(lowestEf_line)
    if max_lowestEf<0.0:
        print(" WARNING(plot_Edef_eFermi)::There is not positive-cros point of Edef.")
        if plot_params_in["Edef_y_upper_limit"]=="AUTO":
            print("    Edef_y_upper_limit is set to 3.0 eV.")
            plot_params_in["Edef_y_upper_limit"]=3.0
    if plot_params_in["Edef_y_upper_limit"]=="AUTO":
        plot_params_in["Edef_y_upper_limit"]=max_lowestEf*2.0
    #### Screening defect species for plotting
    defects_list_screened=[]
    for d1 in defects_list:
        elist1=d1["defect_energy"]
        bool_plot=False
        for i1,eF1 in enumerate(eFermi_list):
            e2=elist1[i1]
            if eF1>plot_params_in["Edef_x_lower_limit"] and eF1<plot_params_in["Edef_x_upper_limit"]\
                    and e2>plot_params_in["Edef_y_lower_limit"] and e2<plot_params_in["Edef_y_upper_limit"]:
                bool_plot=True
        if bool_plot:
            defects_list_screened.append(d1)
    #### Plotting defect-energies without bundling
    fig1=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
    fig2legend=plt.figure(figsize=(plot_params_in["figsize_x_inch"]*0.5,plot_params_in["figsize_x_inch"]*0.5),constrained_layout=True)
    ax1=fig1.add_subplot(111)
    ax1.tick_params(axis="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
    lines=[]
    legends=[]
    for d1 in defects_list_screened:
        l1,=ax1.plot(eFermi_list,d1["defect_energy"],c=d1["line_color"],ls=d1["line_style"],lw=d1["line_width"])
        lines.append(l1)
        legends.append(d1["label_for_legend_withQ_withID"])
    if plot_params_in["Edef_zero_line"]:
        if np.abs(plot_params_in["Edef_y_lower_limit"])>1e-10:
            ax1.axhline(0.0,color="k",ls=":",lw=1.0)
        ax1.axvline(eFermi_balanced,color="k",ls=":",lw=1.0)
    ax1.set_xlim([plot_params_in["Edef_x_lower_limit"],plot_params_in["Edef_x_upper_limit"]])
    ax1.set_ylim([plot_params_in["Edef_y_lower_limit"],plot_params_in["Edef_y_upper_limit"]])
    if plot_params_in["Edef_bands_fill"]:
        if plot_params_in["Edef_x_lower_limit"]<0.0:
            ax1.axvspan(plot_params_in["Edef_x_lower_limit"],0.0,color="gray",alpha=0.2,linewidth=0)
        if plot_params_in["Edef_x_upper_limit"]>Egap:
            ax1.axvspan(Egap,plot_params_in["Edef_x_upper_limit"],color="gray",alpha=0.2,linewidth=0)
    ax1.set_xlabel(plot_params_in["Edef_xlabel"],size=plot_params_in["label_size"])
    ax1.set_ylabel(plot_params_in["Edef_ylabel"],size=plot_params_in["label_size"])
    if plot_params_in["Edef_xtick_labels"]!="NONE":
        ax1.set_xticks(plot_params_in["Edef_xtick_labels"])
    if plot_params_in["Edef_ytick_labels"]!="NONE":
        ax1.set_yticks(plot_params_in["Edef_ytick_labels"])
    num_data=len(defects_list_screened)
    ncol_df=int(np.floor(float(num_data)**0.5))
    fig2legend.legend(lines,legends,ncol=ncol_df,borderaxespad=0,fontsize=plot_params_in["label_size"],
        edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0)
    for f1 in plot_params_in["format"]:
        fig1.savefig(root_outfiles+"_Edef_separated_main."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        fig2legend.savefig(root_outfiles+"_Edef_separated_legend."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
    plt.close(fig1)
    plt.close(fig2legend)

    #### Bundling the same defect-type with a different charge
    defects_list_Qmerged={}
    for d1 in defects_list:
        k1=d1["label_withoutQ"]
        q1=d1["charge"]
        if not k1 in defects_list_Qmerged.keys():
            def1={}
            def1["defect_energy"]=np.zeros(len(eFermi_list))+1e100
            def1["charge_list"]=np.zeros(len(eFermi_list))
            def1["label_for_legend"]=d1["label_for_legend"]
            def1["line_color"]=d1["line_color"]
            def1["line_style"]="-"
            def1["line_width"]=d1["line_width"]
            defects_list_Qmerged[k1]=def1
 
    for i1,eF1 in enumerate(eFermi_list):
        for d1 in defects_list:
            k1=d1["label_withoutQ"]
            e1=d1["defect_energy"][i1]
            q1=d1["charge"]
            e2=defects_list_Qmerged[k1]["defect_energy"][i1]
            if e1<e2:
                defects_list_Qmerged[k1]["defect_energy"][i1]=e1
                defects_list_Qmerged[k1]["charge_list"][i1]=q1
    #### Calculating charge-transition levels
    transition_levels={}
    for k1,d1 in defects_list_Qmerged.items():
        transition_levels[k1]=[]
        elist=d1["defect_energy"]
        qlist=d1["charge_list"]
        for i1,eF1 in enumerate(eFermi_list):
            if i1==0:
                q_prev=qlist[0]
                e_prev=elist[0]
                eF_prev=eF1
                continue
            q_new=qlist[i1]
            e_new=elist[i1]
            if q_new!=q_prev:
                tl1={}
                tl1["q_prev"]=q_prev
                tl1["q_new"]=q_new
                tl1["Fermi_level"]=(eF1+eF_prev)*0.5
                tl1["defect_energy"]=(e_new+e_prev)*0.5
                transition_levels[k1].append(tl1)
            q_prev=q_new
            e_prev=e_new
            eF_prev=eF1
    fout=open(root_outfiles+"_Edef_transition_levels.csv","w")
    fout.write("defect_type,q_prev,q_new,Fermi_level,defect_energy\n")
    for k1,tl1 in transition_levels.items():
        for tl2 in tl1:
            fout.write(k1+",")
            fout.write(str(tl2["q_prev"])+",")
            fout.write(str(tl2["q_new"])+",")
            fout.write(str(tl2["Fermi_level"])+",")
            fout.write(str(tl2["defect_energy"])+"\n")
    fout.close()
    #### Screening defect species for plotting
    defects_list_Qmerged_screened={}
    for k1,d1 in defects_list_Qmerged.items():
        elist1=d1["defect_energy"]
        bool_plot=False
        for i1,eF1 in enumerate(eFermi_list):
            e2=elist1[i1]
            if eF1>plot_params_in["Edef_x_lower_limit"] and eF1<plot_params_in["Edef_x_upper_limit"]\
                    and e2>plot_params_in["Edef_y_lower_limit"] and e2<plot_params_in["Edef_y_upper_limit"]:
                bool_plot=True
        if bool_plot:
            defects_list_Qmerged_screened[k1]=d1

    #### Plotting defect-energies with bundling
    fig1=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
    fig2legend=plt.figure(figsize=(plot_params_in["figsize_x_inch"]*0.5,plot_params_in["figsize_x_inch"]*0.5),constrained_layout=True)
    ax1=fig1.add_subplot(111)
    ax1.tick_params(axis="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
    lines=[]
    legends=[]
    for k1,d1 in defects_list_Qmerged_screened.items():
        l1,=ax1.plot(eFermi_list,d1["defect_energy"],c=d1["line_color"],ls=d1["line_style"],lw=d1["line_width"])
        lines.append(l1)
        legends.append(d1["label_for_legend"])
        if k1 in transition_levels.keys():
            xlist_tl=[]
            ylist_tl=[]
            for tl2 in transition_levels[k1]:
                xlist_tl.append(tl2["Fermi_level"])
                ylist_tl.append(tl2["defect_energy"])
            ax1.plot(xlist_tl,ylist_tl,"o",mfc="w",mec=d1["line_color"])
    if plot_params_in["Edef_zero_line"]:
        if np.abs(plot_params_in["Edef_y_lower_limit"])>1e-10:
            ax1.axhline(0.0,color="k",ls=":",lw=1.0)
        ax1.axvline(eFermi_balanced,color="k",ls=":",lw=1.0)
    ax1.set_xlim([plot_params_in["Edef_x_lower_limit"],plot_params_in["Edef_x_upper_limit"]])
    ax1.set_ylim([plot_params_in["Edef_y_lower_limit"],plot_params_in["Edef_y_upper_limit"]])
    if plot_params_in["Edef_bands_fill"]:
        if plot_params_in["Edef_x_lower_limit"]<0.0:
            ax1.axvspan(plot_params_in["Edef_x_lower_limit"],0.0,color="gray",alpha=0.2,linewidth=0)
        if plot_params_in["Edef_x_upper_limit"]>Egap:
            ax1.axvspan(Egap,plot_params_in["Edef_x_upper_limit"],color="gray",alpha=0.2,linewidth=0)
    ax1.set_xlabel(plot_params_in["Edef_xlabel"],size=plot_params_in["label_size"])
    ax1.set_ylabel(plot_params_in["Edef_ylabel"],size=plot_params_in["label_size"])
    if plot_params_in["Edef_xtick_labels"]!="NONE":
        ax1.set_xticks(plot_params_in["Edef_xtick_labels"])
    if plot_params_in["Edef_ytick_labels"]!="NONE":
        ax1.set_yticks(plot_params_in["Edef_ytick_labels"])
    num_data=len(defects_list_Qmerged_screened)
    ncol_df=int(np.floor(float(num_data)**0.5))
    fig2legend.legend(lines,legends,ncol=ncol_df,borderaxespad=0,fontsize=plot_params_in["label_size"],
        edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0)
    for f1 in plot_params_in["format"]:
        fig1.savefig(root_outfiles+"_Edef_Qmerged_main."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        fig2legend.savefig(root_outfiles+"_Edef_Qmerged_legend."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
    plt.close(fig1)
    plt.close(fig2legend)
    return

def output_density_with_eqcond(dens_in,eqcond_in,out_filename):
    add_list=[]
    for eq1,v1 in eqcond_in.items():
        if eq1.find("P_")==0:
            gas1=eq1.split("_")[1].strip()
            add1=["","","","","pressure_"+gas1,v1]
            add_list.append(add1)
        if eq1.find("lambda_")==0:
            add1=["","","","",eq1,v1]
            add_list.append(add1)
        if eq1.find("fix_Natoms")==0:
            for v2 in v1:
                eq2=eq1+"_"+v2["element"]
                add1=["","","","",eq2,v2["target_Natoms"]]
                add_list.append(add1)
    dens_list=dens_in[:2]+add_list+dens_in[2:]
    if not os.path.exists(out_filename):
        fout=open(out_filename,"w")
        for i1 in range(len(dens_list[0])-1):
            str1=""
            for d1 in dens_list:
                str1+=str(d1[i1])+","
            fout.write(str1[:-1]+"\n")
    else:
        fout=open(out_filename,"a")
    str1=""
    for d1 in dens_list:
        str1+=str(d1[-1])+","
    fout.write(str1[:-1]+"\n")
    fout.close()
    return

def plot_defect_densities(plot_params_in={}):
    if "outfiles_header" in plot_params_in.keys():
        root_outfiles=plot_params_in["outfiles_header"]
    else:
        root_outfiles="plot"
    if "input_filename" in plot_params_in.keys():
        filename_in=plot_params_in["input_filename"]
    else:
        filename_in="out_densities.csv"
    if not os.path.exists(filename_in):
        print(f" ERROR(plot_defect_densities):: density-file not found: {filename_in}")
        sys.exit()
    if not "format" in plot_params_in.keys():
        plot_params_in["format"]=["png"]
    if not "dpi" in plot_params_in.keys():
        plot_params_in["dpi"]=100
    if not "figsize_x_cm" in plot_params_in.keys():
        plot_params_in["figsize_x_cm"]=9.0
    if not "figsize_y_cm" in plot_params_in.keys():
        plot_params_in["figsize_y_cm"]=8.0
    plot_params_in["figsize_x_inch"]=plot_params_in["figsize_x_cm"]/2.54
    plot_params_in["figsize_y_inch"]=plot_params_in["figsize_y_cm"]/2.54
    if not "label_size" in plot_params_in.keys():
        plot_params_in["label_size"]=10
    if not "ticks_size" in plot_params_in.keys():
        plot_params_in["ticks_size"]=8
    if not "ticks_pad" in plot_params_in.keys():
        plot_params_in["ticks_pad"]=4.0
    if not "replace_V_for_Vac" in plot_params_in.keys():
        plot_params_in["replace_V_for_Vac"]=True

    if not "dens_unit_cm3" in plot_params_in.keys():
        plot_params_in["dens_unit_cm3"]=False
    if not "dens_xaxis_parameter" in plot_params_in.keys():
        plot_params_in["dens_xaxis_parameter"]="NONE"
    if not "dens_xaxis_log" in plot_params_in.keys():
        plot_params_in["dens_xaxis_log"]=False
    if not "dens_x_upper_limit" in plot_params_in.keys():
        plot_params_in["dens_x_upper_limit"]="NONE"
    if not "dens_x_lower_limit" in plot_params_in.keys():
        plot_params_in["dens_x_lower_limit"]="NONE"
    if not "dens_xlabel" in plot_params_in.keys():
        plot_params_in["dens_xlabel"]="NONE"
    if not "dens_xtick_labels" in plot_params_in.keys():
        plot_params_in["dens_xtick_labels"]="NONE"
    if not "dens_yaxis_log" in plot_params_in.keys():
        plot_params_in["dens_yaxis_log"]=True
    if not "dens_y_lower_limit" in plot_params_in.keys():
        if plot_params_in["dens_unit_cm3"]:
            plot_params_in["dens_y_lower_limit"]=1e16
        else:
            plot_params_in["dens_y_lower_limit"]=1e-6
    if not "dens_y_upper_limit" in plot_params_in.keys():
        if plot_params_in["dens_unit_cm3"]:
            plot_params_in["dens_y_upper_limit"]=1e22
        else:
            plot_params_in["dens_y_upper_limit"]=1.0
    if not "dens_ylabel" in plot_params_in.keys():
        if plot_params_in["dens_unit_cm3"]:
            plot_params_in["dens_ylabel"]=r"$\mathrm{Defect\ density\ [cm^{-3}]}$"
        else:
            plot_params_in["dens_ylabel"]=r"$\mathrm{Defect\ density\ [/cell]}$"

    if not "Edef_x_lower_limit" in plot_params_in.keys():
        plot_params_in["Edef_x_lower_limit"]=0.0
    if not "Edef_x_upper_limit" in plot_params_in.keys():
        plot_params_in["Edef_x_upper_limit"]="BandGap"
    if not "Edef_y_lower_limit" in plot_params_in.keys():
        plot_params_in["Edef_y_lower_limit"]=0.0
    if not "Edef_y_upper_limit" in plot_params_in.keys():
        plot_params_in["Edef_y_upper_limit"]=3.0
    if not "Edef_ylabel" in plot_params_in.keys():
        plot_params_in["Edef_ylabel"]=r"$\mathrm{Defect\ formation\ energy\ [eV]}$"
    if not "Edef_zero_line" in plot_params_in.keys():
        plot_params_in["Edef_zero_line"]=True
    if not "Edef_bands_fill" in plot_params_in.keys():
        plot_params_in["Edef_bands_fill"]=True
    ####################
    print(" Starting plot_defect_densities")
    fin=open(filename_in).readlines()
    l1=fin.pop(0).strip()
    t1=l1.split(",")
    Egap=-1.0
    Volume=-1.0
    if t1[0].split("=")[0].strip()=="Egap":
        Egap=float(t1[0].split("=")[1].strip())
    if t1[1].split("=")[0].strip()=="Volume":
        Volume=float(t1[1].split("=")[1].strip())
        tocm3=1.0e24/Volume
    if Egap<0.0 or Volume<0.0:
        print("Error: invalid format at line 1 in the input file.")
        sys.exit()
    ####################
    datalist0={}
    key_list0=[]
    for l1 in fin:
        l2=l1.split(",")
        if l2[0].strip()=="parameter":
            for k2 in l2[1:]:
                key_list0.append(k2.strip())
                datalist0[k2.strip()]={}
                datalist0[k2.strip()]["values"]=[]
    for l1 in fin:
        l2=l1.split(",")
        if l2[0].strip()=="parameter":
            continue
        elif l2[0].strip()=="line_color":
            for i2,v2 in enumerate(l2[1:]):
                datalist0[key_list0[i2]]["line_color"]=v2.strip()
        elif l2[0].strip()=="line_style":
            for i2,v2 in enumerate(l2[1:]):
                datalist0[key_list0[i2]]["line_style"]=v2.strip()
        elif l2[0].strip()=="line_width":
            for i2,v2 in enumerate(l2[1:]):
                datalist0[key_list0[i2]]["line_width"]=v2.strip()
        else:
            for i2,v2 in enumerate(l2[1:]):
                datalist0[key_list0[i2]]["values"].append(float(v2.strip()))
    if plot_params_in["dens_xaxis_parameter"]!="NONE":
        if not plot_params_in["dens_xaxis_parameter"] in key_list0:
            print(f" ERROR(plot)::"+plot_params_in["dens_xaxis_parameter"]+" is not found." )
            sys.exit()
    ####################
    print(" Reading eq-conditions")
    parameters_list1={}
    parameters_list2={}
    datalist1={}
    for k1,d1 in datalist0.items():
        d2=d1["values"]
        d3=[]
        for d4 in d2:
            if d4 not in d3:
                d3.append(d4)
        if k1.find("temperature")==0 or k1.find("pressure_")==0 or k1.find("lambda_")==0 or k1.find("fix_Natoms_")==0:
            parameters_list1[k1]=d2
            parameters_list2[k1]=d3
        else:
            datalist1[k1]=d1
    for k1,v1 in parameters_list2.items():
        str_out=f"   {k1}: "
        for v2 in v1:
            str_out+=f"{v2}, "
        print(f"{str_out[:-2]}")
    if plot_params_in["dens_xaxis_parameter"]=="NONE":
        num_max=-1
        param_max=""
        for k1,v1 in parameters_list1.items():
            n1=len(set(v1))
            if n1>num_max:
                num_max=n1
                param_max=k1
        plot_params_in["dens_xaxis_parameter"]=param_max
    bool_fixNatoms_linked=False
    if plot_params_in["dens_xaxis_parameter"].find("fix_Natoms_linked")==0:
        bool_fixNatoms_linked=True
    if plot_params_in["dens_xlabel"]=="NONE":
        if plot_params_in["dens_xaxis_parameter"]=="temperature":
            plot_params_in["dens_xlabel"]=r"Temperature [K]"
        elif plot_params_in["dens_xaxis_parameter"].find("pressure_")==0:
            g1=plot_params_in["dens_xaxis_parameter"].split("_")[1].strip()
            g2=parse_composition_list(g1)
            g4="$\\mathrm{"
            for (at2,nat2) in g2:
                g4=g4+at2+"_{"+str(nat2)+"}"
            g4=g4+"}$"
            plot_params_in["dens_xlabel"]=f"Pressure ({g4}) [Pa]"
        elif plot_params_in["dens_xaxis_parameter"].find("lambda_")==0:
            lab1=plot_params_in["dens_xaxis_parameter"].split("_")[1].strip()
            plot_params_in["dens_xlabel"]="$\lambda$"+f" ({lab1})"
        elif plot_params_in["dens_xaxis_parameter"].find("fix_Natoms_")==0:
            lab1=plot_params_in["dens_xaxis_parameter"].split("_")[-1].strip()
            plot_params_in["dens_xlabel"]="$N_\mathrm{atom}$"+f" ({lab1})"
        else:
            print(f" ERROR(plot)::'dens_xaxis_parameter' cannot be defined.")
            sys.exit()
    parameters_list_main=[]
    parameters_list_exclmain={}
    bool_lambda=False
    if plot_params_in["dens_xaxis_parameter"].find("lambda_")==0:
        bool_lambda=True
    for k1,v1 in parameters_list2.items():
        if k1==plot_params_in["dens_xaxis_parameter"]:
            parameters_list_main=v1
        else:
            if bool_lambda and k1.find("lambda_")==0:
                bool_lambda=False
            else:
                parameters_list_exclmain[k1]=v1
    if len(parameters_list_main)<=3:
        print(f" WARNING(plot)::Num. of dens_xaxis_parameter values is very small!")
    if plot_params_in["dens_x_lower_limit"]=="NONE":
        plot_params_in["dens_x_lower_limit"]=min(parameters_list_main)
    if plot_params_in["dens_x_upper_limit"]=="NONE":
        plot_params_in["dens_x_upper_limit"]=max(parameters_list_main)
    eq_conditions=[]
    eq_conditions_labels=[]
    for k1,v1 in parameters_list_exclmain.items():
        if bool_fixNatoms_linked and k1.find("fix_Natoms_")==0:
            continue
        if len(eq_conditions)==0:
            eq_conditions=v1
        else:
            eq_conditions=product_local(eq_conditions,v1)
        eq_conditions_labels.append(k1)
    fout_conditions=open(root_outfiles+"_plotdens_eqconditions.csv","w")
    str_out=f"ID_eqcond, "
    for ieq1,lab1 in enumerate(eq_conditions_labels):
        str_out+=f"{lab1}, "
    fout_conditions.write(str_out[:-2]+"\n")
    if len(eq_conditions_labels)==1 and isinstance(eq_conditions[0],float):
        tmp1=[]
        for t1 in eq_conditions:
            tmp1.append([t1])
        eq_conditions=tmp1
    for ieq1,eq1 in enumerate(eq_conditions):
        str_out=f"{ieq1+1:0>4}, "
        for eq2 in eq1:
            str_out+=f"{eq2}, "
        fout_conditions.write(str_out[:-2]+"\n")
    fout_conditions.close()
    ####################
    dirname=f"{root_outfiles}_plotdens_data"
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
    os.makedirs(dirname)
    os.chdir(dirname)
    default_color=("crimson","mediumblue","forestgreen","orange","deepskyblue","lime",
                   "darksalmon","aqua","olive","magenta","turquoise","midnightblue",
                   "rosybrown","cornflowerblue","lightslategray","navajowhite","tan")
    for ieq1,eq1 in enumerate(eq_conditions):
        ieq2=ieq1+1
        ieq2_str=f"{ieq2:0>4}"
        dirname=f"eqcond_{ieq2_str}"
        os.makedirs(dirname)
        os.chdir(dirname)
        ### Preparing data
        datalist2={}
        for k1,d1 in datalist1.items():
            datalist2[k1]=copy.deepcopy(d1)
            datalist2[k1]["values"]=[]
            if k1.find("density_")!=0 and k1.find("energy_")!=0:
                continue
            label_def1=k1[k1.find("_")+1:]
            if label_def1=="Hole":
                label_legend="$h^{+}$"
                label_def4="$h^{+}$"
            elif label_def1=="Electron":
                label_legend="$e^{-}$"
                label_def4="$e^{-}$"
            else:
                label_def2=label_def1[1:label_def1.find("]")]
                label_def4=""
                for t1 in label_def2.split("+"):
                    t2=t1.split("_")
                    if t2[0]=="Vac" and plot_params_in["replace_V_for_Vac"]:
                        t2[0]="V"
                    label_def4+="{"+t2[0]+"}_{"+t2[1]+"}+"
                label_def4=label_def4[:-1]
                if "+" in label_def4:
                    label_def4="["+label_def4+"]"
                label_charge=label_def1[label_def1.find("{")+1:label_def1.find("}")]
                label_charge_int=int(label_charge)
                if label_charge_int==-1:
                    label_charge="-"
                elif label_charge_int==1:
                    label_charge="+"
                elif label_charge_int>1:
                    label_charge="+"+label_charge
                elif label_charge_int<-1:
                    label_charge="-"+label_charge[1:]
                label_id=label_def1[label_def1.find("(")+1:label_def1.find(")")]
                label_legend="\mathrm{"+label_def4+"^{"+label_charge+"}}"
                if int(label_id)>0:
                    label_legend=label_legend+"("+label_id+")"
                label_legend="$"+label_legend+"$"
            datalist2[k1]["label_legend_wQ"]=label_legend
            datalist2[k1]["label_legend"]=label_def4
        for ip1 in range(len(parameters_list1[plot_params_in["dens_xaxis_parameter"]])):
            bool_eq1=True
            for ieq3,veq3 in enumerate(eq1):
                v2=parameters_list1[eq_conditions_labels[ieq3]][ip1]
                if bool_fixNatoms_linked and eq_conditions_labels[ieq3].find("fix_Natoms_")==0:
                    continue
                if not math.isclose(v2,veq3,rel_tol=1e-9):
                    bool_eq1=False
            if bool_eq1:
                for k1,d1 in datalist1.items():
                    datalist2[k1]["values"].append(datalist1[k1]["values"][ip1])
        ### Plot-chempot
        fig=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
        ax=fig.add_subplot(111)
        ax.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        icolor=0
        for k1,d1 in datalist2.items():
            if k1.find("chempot_")==0:
                e1=k1.split("_")[1].strip()
                if len(d1["line_color"])==0:
                    d1["line_color"]=default_color[icolor]
                    icolor+=1
                if len(d1["line_style"])==0:
                    d1["line_style"]="-"
                if len(d1["line_width"])==0:
                    d1["line_width"]=1.5
                ax.plot(parameters_list_main,d1["values"],label=e1,c=d1["line_color"],
                           ls=d1["line_style"],lw=d1["line_width"])
        ax.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        if plot_params_in["dens_xaxis_log"]:
            ax.set_xscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax.set_xticks(plot_params_in["dens_xtick_labels"])
        ax.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        ax.set_ylabel(r"$\mathrm{Chemical\ potential,\ }\mu_\mathrm{atom}\ \mathrm{[eV]}$",size=plot_params_in["label_size"])
        ax.legend(loc=0,fontsize=plot_params_in["ticks_size"],edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0)
        for f1 in plot_params_in["format"]:
            fig.savefig(root_outfiles+"_chempots."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig)
        ### Plot-Nsite
        fig=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
        ax=fig.add_subplot(111)
        ax.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        icolor=0
        for k1,d1 in datalist2.items():
            if k1.find("Nsite_")==0:
                e1=k1.split("_")[1].strip()
                if len(d1["line_color"])==0:
                    d1["line_color"]=default_color[icolor]
                    icolor+=1
                if len(d1["line_style"])==0:
                    d1["line_style"]="-"
                if len(d1["line_width"])==0:
                    d1["line_width"]=1.5
                ax.plot(parameters_list_main,d1["values"],label=e1,c=d1["line_color"],
                           ls=d1["line_style"],lw=d1["line_width"])
        ax.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        if plot_params_in["dens_xaxis_log"]:
            ax.set_xscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax.set_xticks(plot_params_in["dens_xtick_labels"])
        ax.ticklabel_format(axis="y",useOffset=True,useMathText=True)
        ax.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        ax.set_ylabel(r"$N_\mathrm{site}\ \mathrm{[/cell]}$",size=plot_params_in["label_size"])
        ax.legend(loc=0,fontsize=plot_params_in["ticks_size"],edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0)
        for f1 in plot_params_in["format"]:
            fig.savefig(root_outfiles+"_Nsites."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig)
        ### Plot-deltaNsite
        fig=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
        ax=fig.add_subplot(111)
        ax.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        icolor=0
        for k1,d1 in datalist2.items():
            if k1.find("delta_Nsite_")==0:
                e1=k1.split("_")[-1].strip()
                if len(d1["line_color"])==0:
                    d1["line_color"]=default_color[icolor]
                    icolor+=1
                if len(d1["line_style"])==0:
                    d1["line_style"]="-"
                if len(d1["line_width"])==0:
                    d1["line_width"]=1.5
                ax.plot(parameters_list_main,d1["values"],label=e1,c=d1["line_color"],
                           ls=d1["line_style"],lw=d1["line_width"])
        ax.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        if plot_params_in["dens_xaxis_log"]:
            ax.set_xscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax.set_xticks(plot_params_in["dens_xtick_labels"])
        ax.ticklabel_format(axis="y",useOffset=True,useMathText=True)
        ax.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        ax.set_ylabel(r"$\delta N_\mathrm{site}\ \mathrm{[/cell]}$",size=plot_params_in["label_size"])
        ax.legend(loc=0,fontsize=plot_params_in["ticks_size"],edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0)
        for f1 in plot_params_in["format"]:
            fig.savefig(root_outfiles+"_Nsites_delta."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig)
        ### Plot-Natom
        fig=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
        ax=fig.add_subplot(111)
        ax.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        icolor=0
        for k1,d1 in datalist2.items():
            if k1.find("Natom_")==0:
                e1=k1.split("_")[1].strip()
                if len(d1["line_color"])==0:
                    d1["line_color"]=default_color[icolor]
                    icolor+=1
                if len(d1["line_style"])==0:
                    d1["line_style"]="-"
                if len(d1["line_width"])==0:
                    d1["line_width"]=1.5
                ax.plot(parameters_list_main,d1["values"],label=e1,c=d1["line_color"],
                           ls=d1["line_style"],lw=d1["line_width"])
        ax.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        if plot_params_in["dens_xaxis_log"]:
            ax.set_xscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax.set_xticks(plot_params_in["dens_xtick_labels"])
        ax.ticklabel_format(axis="y",useOffset=True,useMathText=True)
        ax.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        ax.set_ylabel(r"$N_\mathrm{atom}\ \mathrm{[/cell]}$",size=plot_params_in["label_size"])
        ax.legend(loc=0,fontsize=plot_params_in["ticks_size"],edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0)
        for f1 in plot_params_in["format"]:
            fig.savefig(root_outfiles+"_Natoms."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig)
        ### Plot-deltaNsite
        fig=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
        ax=fig.add_subplot(111)
        ax.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        icolor=0
        for k1,d1 in datalist2.items():
            if k1.find("delta_Natom_")==0:
                e1=k1.split("_")[-1].strip()
                if len(d1["line_color"])==0:
                    d1["line_color"]=default_color[icolor]
                    icolor+=1
                if len(d1["line_style"])==0:
                    d1["line_style"]="-"
                if len(d1["line_width"])==0:
                    d1["line_width"]=1.5
                ax.plot(parameters_list_main,d1["values"],label=e1,c=d1["line_color"],
                           ls=d1["line_style"],lw=d1["line_width"])
        ax.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        if plot_params_in["dens_xaxis_log"]:
            ax.set_xscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax.set_xticks(plot_params_in["dens_xtick_labels"])
        ax.ticklabel_format(axis="y",useOffset=True,useMathText=True)
        ax.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        ax.set_ylabel(r"$\delta N_\mathrm{atom}\ \mathrm{[/cell]}$",size=plot_params_in["label_size"])
        ax.legend(loc=0,fontsize=plot_params_in["ticks_size"],edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0)
        for f1 in plot_params_in["format"]:
            fig.savefig(root_outfiles+"_Natoms_delta."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig)
        ### Plot-eFermi
        fig=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
        ax=fig.add_subplot(111)
        ax.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        icolor=0
        for k1,d1 in datalist2.items():
            if k1.find("Fermi_level")==0:
                if len(d1["line_color"])==0:
                    d1["line_color"]=default_color[icolor]
                    icolor+=1
                if len(d1["line_style"])==0:
                    d1["line_style"]="-"
                if len(d1["line_width"])==0:
                    d1["line_width"]=1.5
                ax.plot(parameters_list_main,d1["values"],c=d1["line_color"],
                           ls=d1["line_style"],lw=d1["line_width"])
        ax.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        if plot_params_in["dens_xaxis_log"]:
            ax.set_xscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax.set_xticks(plot_params_in["dens_xtick_labels"])
        ax.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        if plot_params_in["Edef_x_upper_limit"]=="BandGap":
            plot_params_in["Edef_x_upper_limit"]=Egap
        ax.set_ylim([plot_params_in["Edef_x_lower_limit"],plot_params_in["Edef_x_upper_limit"]])
        if plot_params_in["Edef_bands_fill"]:
            if plot_params_in["Edef_x_lower_limit"]<0.0:
                ax.axhspan(plot_params_in["Edef_x_lower_limit"],0.0,color="gray",alpha=0.2,linewidth=0)
            if plot_params_in["Edef_x_upper_limit"]>Egap:
                ax.axhspan(Egap,plot_params_in["Edef_x_upper_limit"],color="gray",alpha=0.2,linewidth=0)
        ax.axhline(Egap*0.5,color="k",linestyle="--",linewidth=1)
        ax.set_ylabel(r"$\mathrm{Fermi\ level\ [eV]}$",size=plot_params_in["label_size"])
        for f1 in plot_params_in["format"]:
            fig.savefig(root_outfiles+"_FermiLevel."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig)
        ### Plot-total-charge
        fig=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
        ax=fig.add_subplot(111)
        ax.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        icolor=0
        for k1,d1 in datalist2.items():
            if k1.find("Total_charge")==0:
                if len(d1["line_color"])==0:
                    d1["line_color"]=default_color[icolor]
                    icolor+=1
                if len(d1["line_style"])==0:
                    d1["line_style"]="-"
                if len(d1["line_width"])==0:
                    d1["line_width"]=1.5
                ax.plot(parameters_list_main,d1["values"],c=d1["line_color"],
                           ls=d1["line_style"],lw=d1["line_width"])
        ax.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        if plot_params_in["dens_xaxis_log"]:
            ax.set_xscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax.set_xticks(plot_params_in["dens_xtick_labels"])
        ax.set_yscale("symlog",linthresh=10**-20)
        ax.axhline(0.0,color="k",ls=":",lw=1.0)
        ax.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        ax.set_ylabel(r"$\mathrm{Total\ charge\ [e]}$",size=plot_params_in["label_size"])
        for f1 in plot_params_in["format"]:
            fig.savefig(root_outfiles+"_TotalCharage."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig)
        ### Plot-energy
        ###-- Screening defect species for plotting
        defects_list_screened={}
        for k1,d1 in datalist2.items():
            if k1.find("energy_")==0:
                dlist1=d1["values"]
                bool_plot=False
                for i1,p1 in enumerate(parameters_list_main):
                    d2=dlist1[i1]
                    if p1>=plot_params_in["dens_x_lower_limit"] and p1<=plot_params_in["dens_x_upper_limit"]\
                        and d2>plot_params_in["Edef_y_lower_limit"] and d2<plot_params_in["Edef_y_upper_limit"]:
                        bool_plot=True
                if bool_plot:
                    defects_list_screened[k1]=d1
        ###-- Plotting defect-energies without bundling
        fig1=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
        fig2legend=plt.figure(figsize=(plot_params_in["figsize_x_inch"]*0.5,plot_params_in["figsize_x_inch"]*0.5),constrained_layout=True)
        ax1=fig1.add_subplot(111)
        ax1.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        lines=[]
        legends=[]
        for k1,d1 in defects_list_screened.items():
            l1,=ax1.plot(parameters_list_main,d1["values"],c=d1["line_color"],ls=d1["line_style"],lw=d1["line_width"])
            lines.append(l1)
            legends.append(d1["label_legend_wQ"])
        if plot_params_in["Edef_zero_line"]:
            if np.abs(plot_params_in["Edef_y_lower_limit"])>1e-10:
                ax1.axhline(0.0,color="k",ls=":",lw=1.0)
        ax1.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        if plot_params_in["dens_xaxis_log"]:
            ax1.set_xscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax1.set_xticks(plot_params_in["dens_xtick_labels"])
        ax1.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        ax1.set_ylabel(plot_params_in["Edef_ylabel"],size=plot_params_in["label_size"])
        ax1.set_ylim([plot_params_in["Edef_y_lower_limit"],plot_params_in["Edef_y_upper_limit"]])
        num_data=len(defects_list_screened)
        ncol_df=int(np.floor(float(num_data)**0.5))
        fig2legend.legend(lines,legends,ncol=ncol_df,borderaxespad=0,fontsize=plot_params_in["label_size"],
            edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0)
        for f1 in plot_params_in["format"]:
            fig1.savefig(root_outfiles+"_defectFormEnergies_separated."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
            fig2legend.savefig(root_outfiles+"_defectFormEnergies_separated_legend."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig1)
        plt.close(fig2legend)
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
        ### Plot-density
        #### Screening defect species for plotting
        defects_list_screened={}
        for k1,d1 in datalist2.items():
            if k1.find("density_")==0:
                if plot_params_in["dens_unit_cm3"]:
                    d1["values"]=np.array(d1["values"])*tocm3
                dlist1=d1["values"]
                bool_plot=False
                for i1,p1 in enumerate(parameters_list_main):
                    d2=dlist1[i1]
                    if p1>=plot_params_in["dens_x_lower_limit"] and p1<=plot_params_in["dens_x_upper_limit"]\
                        and d2>plot_params_in["dens_y_lower_limit"] and d2<plot_params_in["dens_y_upper_limit"]:
                        bool_plot=True
                if bool_plot:
                    defects_list_screened[k1]=d1
        #### Plotting defect-densities 
        fig1=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
        fig2legend=plt.figure(figsize=(plot_params_in["figsize_x_inch"]*0.5,plot_params_in["figsize_x_inch"]*0.5),constrained_layout=True)
        ax1=fig1.add_subplot(111)
        ax1.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        lines=[]
        legends=[]
        for k1,d1 in defects_list_screened.items():
            l1,=ax1.plot(parameters_list_main,d1["values"],c=d1["line_color"],ls=d1["line_style"],lw=d1["line_width"])
            lines.append(l1)
            legends.append(d1["label_legend_wQ"])
        ax1.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        if plot_params_in["dens_xaxis_log"]:
            ax1.set_xscale("log")
        ax1.set_ylim([plot_params_in["dens_y_lower_limit"],plot_params_in["dens_y_upper_limit"]])
        ax1.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        ax1.set_ylabel(plot_params_in["dens_ylabel"],size=plot_params_in["label_size"])
        if plot_params_in["dens_yaxis_log"]:
            ax1.set_yscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax1.set_xticks(plot_params_in["dens_xtick_labels"])
        num_data=len(defects_list_screened)
        ncol_df=int(np.floor(float(num_data)**0.5))
        fig2legend.legend(lines,legends,ncol=ncol_df,borderaxespad=0,fontsize=plot_params_in["label_size"],
            edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0)
        for f1 in plot_params_in["format"]:
            fig1.savefig(root_outfiles+"_defectDensities_separated."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
            fig2legend.savefig(root_outfiles+"_defectDensities_separated_legend."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig1)
        plt.close(fig2legend)
        os.chdir("../")
    return



