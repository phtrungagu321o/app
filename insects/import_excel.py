import xlrd
from difflib import SequenceMatcher
from . import models
class import_excel_handler():
    def __init__(self, file):
        self.warningMessage = ""
        self.status = ""
        self.excel = xlrd.open_workbook(file_contents=file.read())
        self.read()
        
        self.Validate()
        

    def read(self):
        insect_sheet = self.excel.sheet_by_index(0)
        output = ""
        self.name = []
        self.eName = []
        self.kingdom = []
        self.phylum = []
        self._class = []
        self.order = []
        self.family = []
        self.genus = []
        self.species = []
        self.characteristic = []
        self.distribution = []
        self.value = []
        self.reality = []
        self.protective = []
        self.res = []
        self.existPhylum = []
        self.existClass = []
        self.existOrder = []
        self.existFamily = []
        self.existGenus = []
        self.existSpecies = []
        if (insect_sheet.ncols < 15):
            self.status = False
            return
        try:
            print(insect_sheet.row(0))
            index = 0
            for row in range(insect_sheet.nrows):
                if (row != 0):
                    self.res.append(True)

                    self.existPhylum.append(True)
                    self.existClass.append(True)
                    self.existOrder.append(True)
                    self.existFamily.append(True)
                    self.existGenus.append(True)
                    self.existSpecies.append(True)
                    tmp = self.splitSpace(str(insect_sheet.cell_value(rowx=row, colx=1)))
                    
                    if tmp != "false":
                        self.name.append(tmp)
                    else:
                        self.name.append("")
                        self.res[index] = False
                    tmp = self.splitSpace(str(insect_sheet.cell_value(rowx=row, colx=2)))
                    
                    if tmp != "false":
                        self.eName.append(tmp)
                    else:
                        self.eName.append("")
                        self.res[index] = False
                    tmp = self.splitSpace(str(insect_sheet.cell_value(rowx=row, colx=3)))
                    
                    if tmp != "false":
                        self.kingdom.append(tmp)
                    else:
                        self.kingdom.append("")
                        self.res[index] = False
                    tmp = self.splitSpace(str(insect_sheet.cell_value(rowx=row, colx=4)))
                    
                    if tmp != "false":
                        self.phylum.append(tmp)
                    else:
                        self.phylum.append("")
                        self.res[index] = False
                    tmp = self.splitSpace(str(insect_sheet.cell_value(rowx=row, colx=5)))
                    
                    if tmp != "false":
                        self._class.append(tmp)
                    else:
                        self._class.append("")
                        self.res[index] = False
                    tmp = self.splitSpace(str(insect_sheet.cell_value(rowx=row, colx=6)))
                    
                    if tmp != "false":
                        self.order.append(tmp)
                    else:
                        self.order.append("")
                        self.res[index] = False
                    tmp = self.splitSpace(str(insect_sheet.cell_value(rowx=row, colx=7)))
                    
                    if tmp != "false":
                        self.family.append(tmp)
                    else:
                        self.family.append("")
                        self.res[index] = False
                    tmp = self.splitSpace(str(insect_sheet.cell_value(rowx=row, colx=8)))
                    
                    if tmp != "false":
                        self.genus.append(tmp)
                    else:
                        self.genus.append("")
                        self.res[index] = False
                    tmp = self.splitSpace(str(insect_sheet.cell_value(rowx=row, colx=9)))
                    
                    if tmp != "false":
                        self.species.append(tmp)
                    else:
                        self.species.append("")
                        self.res[index] = False
                    
                    self.characteristic.append(str(insect_sheet.cell_value(rowx=row, colx=10)))
                    self.distribution.append(str(insect_sheet.cell_value(rowx=row, colx=11)))
                    self.value.append(str(insect_sheet.cell_value(rowx=row, colx=12)))
                    self.reality.append(str(insect_sheet.cell_value(rowx=row, colx=13)))
                    self.protective.append(str(insect_sheet.cell_value(rowx=row, colx=14)))
                    
                    index += 1;
        except:
            self.status = False
            return
        self.status = True

    def splitSpace(self, input):
        try:
            while(input[0] == " "):
                input = input[1:]

            while(input[0] == "\t"):
                input = input[1:]

            while(input[len(input)-1] == "\t"):
                input = input[:len(input)-1]

            while(input[len(input)-1] == " "):
                input = input[:len(input)-1]
            return input
        except:
            return "false"

    def Compare(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def Validate(self):
        for i in range(len(self.name)):
            kingdom = models.Kingdom.objects.filter(eName=self.kingdom[0])
            if len(kingdom) > 0:
                phylum = models.Phylum.objects.filter(eName=self.phylum[i])
                if len(phylum) > 0:
                    _class = models.Classes.objects.filter(eName=self._class[i], phylum=self.phylum[i])
                    self.existPhylum[i] = True
                    if len(_class) > 0:
                        order = models.Order.objects.filter(eName=self.order[i], classes=self._class[i])
                        self.existClass[i] = True
                        if len(order) > 0:
                            family = models.Family.objects.filter(eName=self.family[i], order=self.order[i])
                            self.existOrder[i] = True
                            if len(family) > 0:
                                genus = models.Genus.objects.filter(eName=self.genus[i], family=self.family[i])
                                self.existFamily[i] = True
                                if len(genus) > 0:
                                    species = models.InsectTest.objects.filter(eName=self.eName[i], genus=self.genus[i])
                                    self.existGenus[i] = True
                                    if len(species) > 0:
                                        self.res[i] = False
                                        self.warningMessage += "<div class='alert alert-danger'> loài: <strong>" + self.species[i] + "</strong> Đã tồn tại</div>"
                                    else:
                                        tmp = models.InsectTest.objects.filter(eName=self.eName[i])
                                        if len(tmp) > 0:
                                            for index in range(len(tmp)):
                                                self.warningMessage += "<div class='alert alert-warning'>loài: " + self.species[i] + " tồn tại trong <b>" + tmp[index].genus.eName + "</b> : <b> "+ self.genus[i] + " </b> index: "+ str(i+1) +" </div>"
                                                self.res[i] = False
                                        else:
                                            self.existSpecies[i] = False
                                            self.warningMessage += ""
                                else:
                                    tmp = models.Genus.objects.filter(eName=self.genus[i])
                                    if len(tmp) > 0:
                                        for index in range(len(tmp)):
                                            self.res[i] = False
                                            if tmp[index].family.eName != self.family[i]:
                                                print(str(len(tmp[index].family.eName)))
                                                print(tmp[index].family.eName)
                                                print(self.family[i])
                                                print(str(len(self.family[i])))
                                                print("~~~~~~~~~~~~~~~~~~~~~~~~")
                                                self.warningMessage += "<div class='alert alert-warning'>genus: " + self.genus[i] + " tồn tại trong <b>" + tmp[index].family.eName + "</b> : <b> "+ self.family[i] + " </b> index: "+ str(i+1) +" </div>"
                                    else:
                                        self.existGenus[i] = False
                                        self.warningMessage += ""
                            else:
                                tmp = models.Family.objects.filter(eName=self.family[i])
                                if len(tmp) > 0:
                                    for index in range(len(tmp)):
                                        self.res[i] = False
                                        if tmp[index].order.eName != self.order[i]:
                                            print(str(len(tmp[index].order.eName)))
                                            print(tmp[index].order.eName)
                                            print(self.order[i])
                                            print(str(len(self.order[i])))
                                            print("~~~~~~~~~~~~~~~~~~~~~~~~")
                                            self.warningMessage += "<div class='alert alert-warning'>family: " + self.family[i] + " tồn tại trong <b>" + tmp[index].order.eName + "</b> : <b> "+ self.order[i] + " </b> index: "+ str(i+1) +" </div>"
                                else:
                                    self.existFamily[i] = False
                                    self.warningMessage += ""
                        else:
                            tmp = models.Order.objects.filter(eName=self.order[i])
                            if len(tmp) > 0:
                                for index in range(len(tmp)):
                                    self.res[i] = False
                                    if tmp[index].classes.eName != self._class[i]:
                                        self.warningMessage +=  "<div class='alert alert-warning'>order: " + self.order[i] + " tồn tại trong <b>" + tmp[index].classes.eName + "</b> : <b> "+ self._class[i] + " </b> index: "+ str(i+1) +" </div>"
                            else:
                                self.existOrder[i] = False
                                self.warningMessage += ""
                    else: 
                        tmp = models.Classes.objects.filter(eName=self._class[i])
                        if len(tmp) > 0:
                            for index in range(len(tmp)):
                                self.res[i] = False
                                if tmp[index].phylum.eName != self.phylum[i]:
                                    self.warningMessage +=  "<div class='alert alert-warning'>class: " + self._class[i] + " tồn tại trong <b>" + tmp[index].phylum.eName + "</b> : <b> "+ self.phylum[i] + " </b> index: "+ str(i+1) +" </div>"
                        else:
                            self.existClass[i] = False
                            self.warningMessage += ""
                else:
                    self.existPhylum[i] = False
                    self.warningMessage += ""
            else:
                self.warningMessage += ""

    def Import(self):
        for i in range(len(self.name)):
            print(self.res[i])
            if self.res[i] != False:
                if self.existPhylum[i] == False:
                    kingdom = models.Kingdom.objects.all()[0]
                    phylum = models.Phylum(kingdom=kingdom, eName=self.phylum[i], name=self.phylum[i], slug="phylum_" + self.phylum[i].replace(" ", "_"))
                    phylum.save()

                if self.existClass[i] == False:
                    phylum = models.Phylum.objects.filter(eName=self.phylum[i])[0]
                    _class = models.Classes(phylum=phylum, eName=self._class[i], name=self._class[i], slug="class_" + self._class[i].replace(" ", "_"))
                    _class.save()

                if self.existOrder[i] == False:
                    _class = models.Classes.objects.filter(eName=self._class[i])[0]
                    order = models.Order(classes=_class, eName=self.order[i], name=self.order[i], slug="order_" + self.order[i].replace(" ", "_"))
                    order.save()

                if self.existFamily[i] == False:
                    order = models.Order.objects.filter(eName=self.order[i])[0]
                    family = models.Family(order=order, eName=self.family[i], name=self.family[i], slug="family_" + self.family[i].replace(" ", "_"))    
                    family.save()

                if self.existGenus[i] == False:
                    family = models.Family.objects.filter(eName=self.family[i])[0]
                    genus = models.Genus(family=family, eName=self.genus[i], name=self.genus[i], slug="genus_" + self.genus[i].replace(" ", "_"))
                    genus.save()

                if self.existSpecies[i] == False:
                    genus = models.Genus.objects.filter(eName=self.genus[i])[0]
                    insect = models.Insect(genus=genus, eName=self.eName[i], name=self.name[i], slug="insect_" + self.eName[i].replace(" ", "_"), characteristic=self.characteristic[i], value=self.value[i], reality=self.reality[i], protective=self.protective[i], distribution=self.distribution[i])
                    insect.save()
                    self.warningMessage +=  "<div class='alert alert-success'><b>" + self.eName[i] + "</b>  Save succeed</div>"
                    print(self.eName[i] + " Save succeed")

                

    

    