import Algorithm as SA
from Library import *

Web.sidebar.title("MÔ PHỎNG LUYỆN KIM")

Category = Web.sidebar.radio('PHÂN TRANG', ["TRANG CHỦ", "GIẢI THUẬT"])

if Category == "TRANG CHỦ":
    Web.title("TÌM HIỂU VỀ BÀI TOÁN NGƯỜI GIAO HÀNG")
    Web.markdown("### Khái niệm sơ lược về bài toán")
    Web.markdown("""
                   <div style = "text-align: justify;">
                   Bài toán người giao hàng (TSP) là một trong những bài toán kinh điển và đầy thách thức trong
                   lĩnh vực tối ưu hóa. Nó đã thu hút sự quan tâm lớn từ cộng đồng nghiên cứu vì tính ứng dụng
                   rộng rãi của nó trong nhiều lĩnh vực thực tế. Tính chất cơ bản của bài toán là cho một tập
                   hợp các thành phố và khoảng cách giữa chúng, tìm một hành trình qua tất cả các thành phố sao
                   cho tổng khoảng cách là nhỏ nhất, và người giao hàng chỉ được đi qua mỗi thành phố đúng một
                   lần trước khi quay lại thành phố xuất phát.
                   </div>""", unsafe_allow_html=True)
    Web.image(image="./Static/TSP Map.png", caption="Minh họa về bài toán Traveling Salesman Problem")
    Web.markdown("""
                   <div style = "text-align: justify;">
                   Đây không chỉ là một vấn đề lý thuyết, mà còn là một vấn đề thực tế quan trọng trong nhiều
                   lĩnh vực, từ vận tải đến lập lịch sản xuất và quản lý chuỗi cung ứng. Trong lĩnh vực vận
                   tải, giải quyết TSP có thể giúp tối ưu hóa lộ trình giao hàng, giảm thiểu chi phí nhiên liệu
                   và thời gian di chuyển. Trong lĩnh vực sản xuất, TSP có thể được sử dụng để tối ưu hóa quy
                   trình sản xuất và giao nhận hàng hóa. Trong lĩnh vực quản lý chuỗi cung ứng, giải quyết TSP
                   có thể giúp cải thiện quy trình vận chuyển và lưu kho.
                   </div>""", unsafe_allow_html=True)

    Web.markdown("### Thuật toán hay cho bài toán")
    Web.markdown("""
                   <div style="text-align: justify;">
                   Để xử lý bài toán dạng này, có rất nhiều phương pháp được áp dụng. Một trong số đó là thuật
                   toán di truyền (genetic algorithm), một phương pháp được lấy cảm hứng từ quá trình tiến hóa
                   trong tự nhiên. Thuật toán di truyền tạo ra một tập hợp các giải pháp (các cá thể), sau đó
                   áp dụng các toán tử tiến hóa như lai ghép (crossover) và đột biến (mutation) để tạo ra các
                   thế hệ con tiếp theo, từ đó dần dần cải thiện giải pháp cho tới khi đạt được kết quả tối ưu
                   hoặc đạt được điều kiện dừng.
                   </div>
                   """, unsafe_allow_html=True)
    Web.image(image="./Static/GA Description.png", caption="Mô tả cách hoạt động của thuật toán GA")

    Web.markdown("""
                   <div style = "text-align: justify;">
                   Ngoài ra, còn có các thuật toán tìm kiếm cục bộ như thuật toán tìm kiếm giải phỏng (simulated
                   annealing), một phương pháp lấy cảm hứng từ quá trình làm mát giả lập trong kim loại. Thuật
                   toán này giúp khai thác không gian giải pháp một cách thông minh, di chuyển từ các giải pháp
                   kém sang các giải pháp tốt hơn dựa trên một hàm mục tiêu và một tham số "nhiệt độ" giả định.
                   </div>""", unsafe_allow_html=True)
    Web.image(image="./Static/SA Description.png", caption="Mô tả cách hoạt động của thuật toán SA")

    Web.markdown("""
                   <div style = "text-align: justify;">
                   Dù có nhiều phương pháp khác nhau, việc chọn phương pháp thích hợp cho một bài toán cụ thể
                   đòi hỏi sự hiểu biết sâu sắc về đặc điểm của bài toán, cũng như sự đánh giá kỹ lưỡng về hiệu
                   suất và thời gian thực thi của các thuật toán. Đối với những bài toán lớn với hàng trăm hoặc
                   hàng nghìn thành phố, việc tìm ra được giải pháp tối ưu có thể trở thành một thách thức đáng
                   kể và việc kết hợp các phương pháp có thể là cách tiếp cận hiệu quả nhất để đạt được kết quả
                   tốt nhất có thể.
                   </div>""", unsafe_allow_html=True)

elif Category == "GIẢI THUẬT":
    Web.title("THUẬT TOÁN MÔ PHỎNG LUYỆN KIM")
    Web.write("Nhập ma trận trọng số và các thông số đầu vào cho bài toán")
    File = Web.file_uploader(label="Nhập vào file ma trận ", type=['TXT'])
    Maximum_Temperature = Web.text_input(label="Nhiệt độ ban đầu", placeholder="VD: 10000")
    Minimum_Temperature = Web.text_input(label="Nhiệt độ lúc sau", placeholder="VD: 0.0001")
    Cooling_Rate = Web.text_input(label="Hệ số làm lạnh(làm mát)", placeholder="VD: 0.9999")

    Params = [Maximum_Temperature, 
              Minimum_Temperature, 
              Cooling_Rate]

    if Web.button("Thực thi chương trình"):
        Annealing = SA.Simulated_Annealing()
        Annealing.Import_Data(File, Params)
        Annealing.Annealing_Execution()
        Annealing.Export_Result()
        Annealing.Export_RunLog()

def Clean_Cache():
    if os.path.exists('__PYCACHE__'): 
        shutil.rmtree('__PYCACHE__')

atexit.register(Clean_Cache)