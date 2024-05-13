from Library import *

def Is_Float(Number):
    try:
        float(Number)
        return True
    except ValueError:
        return False

class Simulated_Annealing:
    def __init__(self):
        self.Initial_Cycle = []
        self.Initial_Distance = None
        self.Optimal_Cycle = []
        self.Optimal_Distance = None
        self.Log = []
        self.Matrix = None
        self.Number = None
        self.Maximum_Temperature = None
        self.Cooling_Rate = None
        self.Minimum_Temperature = None

    def Import_Matrix(self, File):

        def Is_Symmetric():
            Temp = copy.deepcopy(self.Matrix)
            Temp = np.array(Temp)
            return np.array_equal(Temp,Temp.T)
        
        File = File.getvalue().decode("utf-8")
        Lines = File.split("\n")
        self.Number = len(Lines)
        self.Matrix = [[0]*self.Number for _ in range(self.Number)]
        for Row in range(self.Number):
            Line = Lines[Row].split()
            if len(Line) != self.Number:
                Web.error(str(ValueError(f"Số phần tử hàng {Row} khác {self.Number} phần tử")))
                exit(0)
            elif Is_Float(Line[Row]) == False or float(Line[Row]) != 0:
                Web.error(str(ValueError(f"Phần tử ở đường chéo chính hàng {Row} khác không")))
                exit(0)
            else:
                for Col in range(len(Line)):
                    if Is_Float(Line[Col]):
                        self.Matrix[Row][Col] = float(Line[Col])
                    else:
                        Web.error(str(ValueError(f"Ký tự '{Line[Col]}'(R:{Row}, C{Col}) lỗi")))
                        exit(0)

        if Is_Symmetric() == False:
            Web.error(str(ValueError("Ma trận không đối xứng")))
            exit(0)

    def Import_Parameter(self ,Parameters):
        for Item in Parameters:
            if(len(Item) == 0):
                Web.error("Trường nhập đang rỗng, vui lòng nhập!!!")
                exit(0)
            elif Is_Float(Item) == False:
                Web.error(f"Không thể chuyển {Item} sang số thực!!!")
                exit(0)
        self.Maximum_Temperature = float(Parameters[0])
        self.Minimum_Temperature = float(Parameters[1])
        self.Cooling_Rate = float(Parameters[2])

    def Import_Data(self, File, Params):
        if File is not None:
            self.Import_Matrix(File)
        else:
            Web.error("Tệp tin không tồn tại, vui lòng tải lại file")
            exit(0)    
        self.Import_Parameter(Params)
        Web.success("Ma trận trọng số và các thông số nhập là hợp lệ")
    
    def Export_Result(self):
        with Temp.NamedTemporaryFile(delete=False, suffix='.txt') as File:
            File.write("QUÁ TRÌNH MÔ PHỎNG LUYỆN KIM(SA)\n\n\n".encode())
            Label1 = "Khoảng cách:"
            Label2 = "Chu trình:"
            File.write(f"{'':<30}{Label1:<30}{Label2}\n".encode())
            File.write(
                f"{'Chu trình khởi đầu:':<30}{self.Initial_Distance:<30}{self.Initial_Cycle}\n".encode())
            File.write(
                f"{'Chu trình tốt nhất:':<30}{self.Optimal_Distance:<30}{self.Optimal_Cycle}\n".encode())
            File.write("Danh sách cung:\n".encode())
            Label3 = "Chu trình Ban đầu:"
            Label4 = "Chu trình tối ưu:"
            File.write(f"{'':<30}{Label3:<30}{Label4:<30}\n".encode())
            for i in range(self.Number-1):
                uf = self.Initial_Cycle[i]
                vf = self.Initial_Cycle[i+1]
                wf = self.Matrix[uf][vf]
                uo = self.Optimal_Cycle[i]
                vo = self.Optimal_Cycle[i+1]
                wo = self.Matrix[uo][vo]
                Linef = f"{uf} <-> {vf} = {wf}"
                Lineo = f"{uo} <-> {vo} = {wo}"
                File.write(f"{'':<30}{Linef:<30}{Lineo:<30}\n".encode())
            uf = self.Initial_Cycle[-1]
            vf = self.Initial_Cycle[0]
            wf = self.Matrix[uf][vf]
            uo = self.Optimal_Cycle[-1]
            vo = self.Optimal_Cycle[0]
            wo = self.Matrix[uo][vo]
            Linef = f"{uf} <-> {vf} = {wf}"
            Lineo = f"{uo} <-> {vo} = {wo}"
            File.write(f"{'':<30}{Linef:<30}{Lineo:<30}\n".encode())

        with open(File.name, 'r') as File:
            File_Content = File.read()

        Web.download_button("Lưu kết quả.", 
                             File_Content, 
                             "Result.txt", 
                             "text/plain")
        os.remove(File.name)
        
    def Export_RunLog(self):
        with Temp.NamedTemporaryFile(delete=False, suffix='.txt') as File:
            File.write("QUÁ TRÌNH MÔ PHỎNG LUYỆN KIM(SA)\n\n\n".encode())
            Temperature = "Nhiệt độ:"
            Distance = "Khoảng cách:"
            Cycle = "Chu trình:"
            File.write(f"{Temperature:<30}{Distance:<30}{Cycle}\n".encode())
            for Item in self.Log:
                File.write(f"{Item[0]:<30}{Item[1]:<30}{Item[2]}\n".encode())
        
        with open(File.name, 'r') as File:
            File_Content = File.read()

        Web.download_button("Lưu nhật ký.", 
                             File_Content, 
                             "History.txt", 
                             "text/plain")
        os.remove(File.name)

    def Create_Initial_Cycle(self):
        self.Initial_Cycle = self.Nearest_Neighbor()
        self.Initial_Distance = self.Cycle_Distance(self.Initial_Cycle)

    def Nearest_Neighbor(self):
        Unvisited_Cities = list(range(self.Number))
        Current_City = random.choice(Unvisited_Cities)
        Cycle = [Current_City]
        Unvisited_Cities.remove(Current_City)
        while Unvisited_Cities:
            Nearest_City = min(Unvisited_Cities, key=lambda City: self.Matrix[Current_City][City])
            Cycle.append(Nearest_City)
            Current_City = Nearest_City
            Unvisited_Cities.remove(Current_City)
        return Cycle
    
    def Cycle_Distance(self, Array):
        Distance = 0
        for i in range(self.Number-1):
            Distance += self.Matrix[Array[i]][Array[i+1]]
        return Distance + self.Matrix[Array[-1]][Array[0]]
    
    def Convert_To_Matrix(self, Array):
        Cycle_Matrix = [[0 for C in range(self.Number)] for R in range(self.Number)]
        Cycle_Matrix[Array[-1]][Array[0]] = self.Matrix[Array[-1]][Array[0]]
        for i in range(self.Number-1):
            Cycle_Matrix[Array[i]][Array[i+1]] = self.Matrix[Array[i]][Array[i+1]]
        return Cycle_Matrix
    
    def Create_Random_Cycle(self, Array):
        New_Array = copy.deepcopy(Array)
        First, End = sorted(random.sample(range(self.Number), 2))
        New_Array[First:End+1] = reversed(New_Array[First:End+1])
        return New_Array

    def Acceptance(self, Delta, Current_Temperature):
        return np.exp(- Delta / Current_Temperature)
    
    def Annealing(self):
        self.Create_Initial_Cycle()
        self.Cycle_Graph_TSP_SA(self.Initial_Cycle, "Đồ thị chu trình khởi đầu")
        Current_Temperature = self.Maximum_Temperature
        Current_Cycle = self.Initial_Cycle[:]
        Current_Distance = self.Initial_Distance
        Distances = []
        Distances.append(self.Initial_Distance)
        self.Log.append([self.Maximum_Temperature, self.Initial_Distance, self.Initial_Cycle])
        while Current_Temperature >= self.Minimum_Temperature:
            Candidate_Cycle = self.Create_Random_Cycle(Current_Cycle)
            Candidate_Distance = self.Cycle_Distance(Candidate_Cycle)
            Delta = Candidate_Distance - Current_Distance
            if Delta < 0 or self.Acceptance(Delta, Current_Temperature) > random.random():
                Current_Cycle = Candidate_Cycle[:]
                Current_Distance = Candidate_Distance
            Current_Temperature *= self.Cooling_Rate
            Distances.append(Current_Distance)
            self.Log.append([Current_Temperature, Current_Distance, Current_Cycle])
        self.Optimal_Cycle = Current_Cycle[:]
        self.Optimal_Distance = Current_Distance
        self.Cycle_Graph_TSP_SA(self.Optimal_Cycle, "Đồ thị chu trình sau cùng")

    def Cycle_Graph_TSP_SA(self, Array, Name_Image):
        New_Matrix = self.Convert_To_Matrix(Array)
        New_Graph = nx.Graph()
        plt.figure(figsize=(10, 10))
        plt.title(Name_Image, fontsize=20, fontweight="bold")
        for i in range(self.Number):
            for j in range(self.Number):
                w = New_Matrix[Array[i]][Array[j]]
                if w != 0:
                    New_Graph.add_edge(u_of_edge=Array[i], v_of_edge=Array[j], weight=w)
        Layout = nx.layout.circular_layout(New_Graph)
        nx.draw(New_Graph, Layout, with_labels=True, node_size=200, node_color='yellow')
        
        with Temp.NamedTemporaryFile(delete=False, suffix='.png') as Image:
            Path_Image = Image.name
            plt.savefig(Path_Image)
        
        Web.image(Path_Image, Name_Image)
        os.remove(Path_Image)

    def Annealing_Execution(self):
        Progress_Bar = Web.progress(0)
        Spinner = Web.spinner("Chương trình đang chạy, vui lòng đợi giây trong lát")
        with Spinner:
            self.Annealing()
            for Percent_Complete in range(100):
                Progress_Bar.progress(Percent_Complete + 1, f"{Percent_Complete + 1}%")
        Web.success("Chương trình thực thi hoàn tất")