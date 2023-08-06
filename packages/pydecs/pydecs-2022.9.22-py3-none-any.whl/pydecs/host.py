#!/usr/bin/env python
#---------------------------------------------------------------------------
# Copyright 2021 Takafumi Ogawa
# Licensed under the Apache License, Version2.0.
#---------------------------------------------------------------------------
# pydecs-host module
#---------------------------------------------------------------------------
import os,sys
import copy
import numpy as np
from scipy.special import expit

class Host:
    
    def __init__(self,input_host,input_paths=["./"]):
        print(" Reading host-information")
        print(" Lattice-sites")
        self.lattice_sites={}
        for t1 in input_host["site"]:
            k1=t1.pop("label")
            self.lattice_sites[k1]=copy.deepcopy(t1)
            str1=f"   {k1:>3}:: "
            for k2,v2 in t1.items():
                str1+=f"{k2} = {v2:<4}; "
            print(str1[:-2])
            self.lattice_sites[k1]["num_in_defective_cell"]=self.lattice_sites[k1]["num_in_cell"]
        fndos="NONE"
        for path1 in input_paths:
            fn1=path1+"inpydecs_dos.csv"
            if os.path.exists(fn1):
                fndos=fn1
        if fndos=="NONE":
            print(" ERROR:: not-found inpydecs_dos.csv")
            sys.exit()

        self.elements_host=[]
        for k1,s1 in self.lattice_sites.items():
            e1=s1["occ_atom"]
            if e1=="NONE":
                continue
            if not e1 in self.elements_host:
                self.elements_host.append(e1)

        print(" DOS-filename: "+fndos)
        fin = open(fndos)
        l1=fin.readline()
        self.dosList=[]
        self.eneList=[]
        while l1:
            l2=l1.strip()
            if len(l2)==0:
                l1=fin.readline()
                continue
            if l2[0]=="#":
                if "Egap" in l2:
                    self.Egap=float(l2.split("=")[1].split()[0])
                if "EVBM" in l2:
                    self.EVBM=float(l2.split("=")[1].split()[0])
                if "Volume" in l2:
                    self.Volume=float(l2.split("=")[1].split()[0])
            else:
                l2=l2.split(",")
                self.eneList.append(float(l2[0])-self.EVBM)
                self.dosList.append(float(l2[1]))
            l1=fin.readline()
        self.ene_delta=self.eneList[1]-self.eneList[0]
        print(f" Volume = {self.Volume}")
        print(f" Egap = {self.Egap}")
        print(f" EVBM (in dos-file) = {self.EVBM}")
        print(f" NEDOS= {len(self.dosList)}")
        print(f"-"*100)

    def calc_electronic_carrier_densities(self,temperature_in,eFermi_in):
        ikT=1.0/(temperature_in*8.61733262e-5)
        self.dens_elec = 0.0
        self.dens_hole = 0.0
        for i1,e1 in enumerate(self.eneList):
            d1=self.dosList[i1]
            e2=(e1-eFermi_in)*ikT
            if e1>self.Egap*0.8:
                if d1>1e-10:
                    d2=d1*self.ene_delta*expit(-1.0*e2)
                    # d3=d1*self.ene_delta/(np.exp(e2)+1.0)
                    self.dens_elec+=d2
            if e1<self.Egap*0.2:
                if d1>1e-10:
                    d2=d1*self.ene_delta*expit(e2)
                    # d3=d1*self.ene_delta/(np.exp(-1.0*e2)+1.0)
                    self.dens_hole+=d2
        return (self.dens_hole,self.dens_elec)
    
    def get_hole_density(self):
        return self.dens_hole

    def get_electron_density(self):
        return self.dens_elec

    def cell_to_cm3(self,num1_in):
        return float(num1_in)/self.Volume*1.0e24

    def get_Volume(self):
        return self.Volume
    
    def get_EVBM(self):
        return self.EVBM

    def get_Egap(self):
        return self.Egap

    def get_siteList(self):
        return self.lattice_sites.keys()

    def get_atom_at_site(self,site_in):
        return self.lattice_sites[site_in]["occ_atom"]

    def get_Nsite_perfect(self,site_in):
        return self.lattice_sites[site_in]["num_in_cell"]

    def get_Nsites_perfect(self):
        site_list={}
        for s1 in self.lattice_sites.keys():
            site_list[s1]=self.lattice_sites[s1]["num_in_cell"]
        return site_list

    def get_Nsite_defective(self,site_in):
        return self.lattice_sites[site_in]["num_in_defective_cell"]

    def add_Nsite_defective(self,site_in,value_in):
        self.lattice_sites[site_in]["num_in_defective_cell"]+=value_in
        return

    def get_Nsites_defective(self):
        site_list={}
        for s1 in self.lattice_sites.keys():
            site_list[s1]=self.lattice_sites[s1]["num_in_defective_cell"]
        return site_list

    def reset_Nsites_defective(self):
        site_list={}
        for s1 in self.lattice_sites.keys():
            self.lattice_sites[s1]["num_in_defective_cell"]=self.lattice_sites[s1]["num_in_cell"]
            site_list[s1]=self.lattice_sites[s1]["num_in_defective_cell"]
        return 

    def get_elements(self):
        return self.elements_host
