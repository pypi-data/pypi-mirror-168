#!/usr/bin/env python
#---------------------------------------------------------------------------
# Copyright 2021 Takafumi Ogawa
# Licensed under the Apache License, Version2.0.
#---------------------------------------------------------------------------
# pydecs-defects module
#---------------------------------------------------------------------------
import os,sys
import copy
import random
import numpy as np
from scipy.special import expit

from pydecs.host import Host

class Defects:

    def parse_composition(self,comp_in):
        comp1=[]
        ic0=0
        for ic1,c1 in enumerate(comp_in):
            if ic1!=0 and c1.isupper():
                comp1.append(comp_in[ic0:ic1])
                ic0=ic1
        comp1.append(comp_in[ic0:])
        atomList={}
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
            atomList[elem1]=int(num1)
        return atomList

    def parse_defectType(self,defType_in):
        defTypeList=defType_in.split("+")
        deltaNum_atoms={}
        for e1 in self.elemsList:
            deltaNum_atoms[e1]=0.0
        occ_sites={}
        for s1 in self.host.get_siteList():
            occ_sites[s1]=0.0
        for d1 in defTypeList:
            addAtoms1=d1.split("_")[0].strip()
            addAtoms2=self.parse_composition(addAtoms1)
            for at3,n3 in addAtoms2.items():
                if at3=="Vac":
                    continue
                if not at3 in deltaNum_atoms.keys():
                    deltaNum_atoms="DESELECTED"
                    return (deltaNum_atoms,occ_sites)
                deltaNum_atoms[at3]+=n3
            occSite1=d1.split("_")[1].strip()
            site2=""
            if "-" in occSite1:
                occSite2=occSite1.split("-")
                site2=occSite2[0]
                occ2=float(occSite2[1])
            else:
                site2=occSite1
                occ2=1.0
            if not site2 in occ_sites.keys():
                print(" ERROR during reating defect-file::")
                print("    defect_type occupy unknown site: "+defType_in)
                sys.exit()
            occ_sites[site2]=occ2
            at2=self.host.get_atom_at_site(site2)
            if at2 in deltaNum_atoms.keys():
                deltaNum_atoms[at2]-=occ2
        return (deltaNum_atoms,occ_sites)

    def __init__(self,host_in,elemsList_in,input_paths=["./"]):
        print(" Reading defects-information")
        self.host=host_in
        self.elemsList=elemsList_in
        for e1 in self.host.get_elements():
            if not e1 in self.elemsList:
                print(" ERROR(defects):: (a part of) host-elements iss not found in input-elements")
                sys.exit()
        
        fnin="NONE"
        for path1 in input_paths:
            if os.path.exists(path1+"inpydecs_defects.csv"):
                fnin=path1+"inpydecs_defects.csv"
                break
        if fnin=="NONE":
            print(" ERROR::file not-found: inpydecs_defects.csv")
            sys.exit()
        print(" Reading file: "+fnin)
        fin=open(fnin).readlines()
        columns=[ t1.strip() for t1 in fin[0].split(",")]
        column_names=set(["commentout","defect_type","charge","energy_defect","energy_perfect"
            ,"energy_correction","multiplicity","line_color","line_style","line_width"])
        for c1 in column_names:
            if not c1 in columns:
                print(" ERROR::column_not_found: "+c1)
                sys.exit()
        defects0=[]
        for l1 in fin[1:]:
            l2=[ t1.strip() for t1 in l1.split(",")]
            df0={}
            for i3,l3 in enumerate(l2):
                c3=columns[i3]
                if c3=="commentout":
                    df0[c3]=l3
                if c3=="defect_type":
                    df0[c3]=l3
                if c3=="charge":
                    df0[c3]=l3
                if c3=="energy_defect":
                    df0[c3]=l3
                if c3=="energy_perfect":
                    df0[c3]=l3
                if c3=="energy_correction":
                    df0[c3]=l3
                if c3=="multiplicity":
                    df0[c3]=l3
                if c3=="line_color":
                    df0[c3]=l3
                if c3=="line_style":
                    df0[c3]=l3
                if c3=="line_width":
                    df0[c3]=l3
            if len(df0["commentout"])==0 and len(df0["defect_type"])>0:
                for c3 in ["charge","energy_defect","energy_perfect","energy_correction","multiplicity"]:
                    df0[c3]=float(df0[c3]) 
                defects0.append(df0)

        self.data_defects={}
        for df0 in defects0:
            defType1=df0["defect_type"]
            q1=df0["charge"]
            id1=0
            for k1 in self.data_defects.keys():
                if k1[0]==defType1 and k1[1]==q1:
                    id1+=1
            key1=(defType1,q1,id1)
            df1={}
            df1["defect_energy_0"]=df0["energy_defect"]-df0["energy_perfect"]\
                               +df0["energy_correction"]+q1*self.host.get_EVBM()
            df1["charge"]=df0["charge"]
            df1["multiplicity"]=df0["multiplicity"]
            df1["multiplicity_invlog"]=np.log(1.0/df0["multiplicity"])
            df1["line_color"]=df0["line_color"]
            df1["line_style"]=df0["line_style"]
            df1["line_width"]=df0["line_width"]
            (deltaNum_atoms,occ_sites)=self.parse_defectType(defType1)
            df1["deltaNum_atoms"]=deltaNum_atoms
            df1["occ_sites"]=occ_sites
            df1["defect_energy"]="NONE"
            df1["defect_density"]="NONE"
            if deltaNum_atoms!="DESELECTED":
                self.data_defects[key1]=df1
        ###!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # check!!! self.elemsList
        elements_host=self.host.get_elements()
        counts={}
        for e1 in self.elemsList:
            counts[e1]=0
        for k1,df1 in self.data_defects.items():
            for e1,deln in df1["deltaNum_atoms"].items():
                if not e1 in elements_host and deln<-0.1:
                    print(f"ERROR(defects):: not-host-element is removed: {k1[0]}")
                    sys.exit()
                counts[e1]+=deln
        for e1 in self.elemsList:
            if e1 in elements_host:
                continue
            if counts[e1]==0:
                print(f"ERROR(defects):: defect-setting is not found for element({e1})")
                sys.exit()
        ###!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        default_color=("crimson","mediumblue","forestgreen","orange","deepskyblue","lime",
                       "darksalmon","aqua","olive","magenta","turquoise","midnightblue",
                       "rosybrown","cornflowerblue","lightslategray","navajowhite","tan")
        default_style=("-",":","--","-.")
        default_width=1.5
        corresp_colors={}
        i_color=0
        for k1,df1 in self.data_defects.items():
            lc1=df1["line_color"]
            if len(lc1)==0:
                if k1[0] in corresp_colors.keys():
                    df1["line_color"]=corresp_colors[k1[0]]
                else:
                    corresp_colors[k1[0]]=default_color[i_color]
                    df1["line_color"]=corresp_colors[k1[0]]
                    i_color+=1
            ls1=df1["line_style"]
            if len(ls1)==0:
                irnd=random.randint(0,3)
                df1["line_style"]=default_style[irnd]
            lw1=df1["line_width"]
            if len(lw1)==0:
                df1["line_width"]=default_width
        print("-"*100)

    def update_defect_energies_densities(self,temperature_in,chempots_in,eFermi_in):
        ikT=1.0/(temperature_in*8.61733262e-5)
        for k1,df1 in self.data_defects.items():
            df1["defect_energy"] = df1["defect_energy_0"]+df1["charge"]*eFermi_in
            for ie1,e1 in enumerate(self.elemsList):
                df1["defect_energy"]-=df1["deltaNum_atoms"][e1]*chempots_in[e1]
            site2=list(df1["occ_sites"].keys())[0]
            #####legacy-style?? This produces RuntimeWarning in exp()
            #t2 = 1.0/df1["multiplicity"]
            #e2=ikT*df1["defect_energy"]
            #if e2<200.0:
            #    df1["defect_density"] = self.host.get_Nsite_defective(site2)/(1.0+t2*np.exp(e2))
            #else:
            #    df1["defect_density"] = 0.0

            t2 = df1["multiplicity_invlog"]
            e2=t2+ikT*df1["defect_energy"]
            df1["defect_density"] = self.host.get_Nsite_defective(site2)*expit(-1.0*e2)
        return

    def calc_Natoms(self):
        self.Natoms_list={}
        self.Natoms_list_host={}
        for e1 in self.elemsList:
            self.Natoms_list[e1]=0.0
            self.Natoms_list_host[e1]=0.0
        for s1 in self.host.get_siteList():
            at1=self.host.get_atom_at_site(s1)
            if at1 in self.elemsList:
                self.Natoms_list[at1]+=self.host.get_Nsite_perfect(s1)
                self.Natoms_list_host[at1]+=self.host.get_Nsite_perfect(s1)
        for k1,df1 in self.data_defects.items():
            for e1 in self.elemsList:
                self.Natoms_list[e1]+=df1["deltaNum_atoms"][e1]*df1["defect_density"]
        return (self.Natoms_list,self.Natoms_list_host)

    def get_Jacobian(self,elems_in,temperature_in):
        kT=(temperature_in*8.61733262e-5)
        ikT=1.0/kT
        jacob_out=[]
        for e1 in elems_in:
            jacob_tmp=[]
            for e2 in elems_in:
                jac1=0.0
                for k1,df1 in self.data_defects.items():
                    gtmp1=kT*(df1["multiplicity"]*np.exp(-1.0*df1["defect_energy"]*ikT)+1.0)
                    g1=(df1["deltaNum_atoms"][e1]*df1["deltaNum_atoms"][e2]*df1["defect_density"])/gtmp1
                    jac1+=g1
                jacob_tmp.append(jac1)
            jacob_out.append(jacob_tmp)
        return jacob_out

    def get_Natoms_list(self):
        return self.Natoms_list

    def get_defect_types(self):
        return self.data_defects.keys()

    def get_label(self,defType_in):
        str1="["+defType_in[0]+"]^{"+str(int(defType_in[1]))+"}"+"("+str(int(defType_in[2]))+")"
        return str1

    def get_defect_energy(self,defType_in):
        return self.data_defects[defType_in]["defect_energy"]

    def get_defect_density(self,defType_in):
        return self.data_defects[defType_in]["defect_density"]

    def get_charge(self,defType_in):
        return self.data_defects[defType_in]["charge"]

    def get_occ_sites(self,defType_in):
        return self.data_defects[defType_in]["occ_sites"]

    def check_minus_defect_energy(self):
        bool_out=False
        for k1,df1 in self.data_defects.items():
            e1=df1["defect_energy"]
            if e1<0.0:
                print(" WARMING(defects):: There is minus defect formation energy.")
                print("    E_def( "+self.get_label(k1)+" ) = "+str(e1))
                bool_out=True
        return bool_out

    def get_line_color(self,defType_in):
        return self.data_defects[defType_in]["line_color"]

    def get_line_style(self,defType_in):
        return self.data_defects[defType_in]["line_style"]

    def get_line_width(self,defType_in):
        return self.data_defects[defType_in]["line_width"]

