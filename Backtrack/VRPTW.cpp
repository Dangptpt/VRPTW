// Date created: "18:04:03, 27-12-2023"
// Code by Dangptpt_
#include<bits/stdc++.h>

using namespace std;

#define fi first
#define se second
#define pb push_back

typedef long long LL;
typedef unsigned long long ULL;
typedef pair <int, int> II;

template <typename T> void read(T &t) {
    t = 0; char ch = getchar(); int f = 1;
    while (!isdigit(ch)) { if (ch == '-') f = -1; ch = getchar(); }
    do { (t *= 10) += ch - '0'; ch = getchar(); } while (isdigit(ch)); t *= f;
}

const int MAXN = 1 + 1e6;
const int mod = 1e9 + 7;
const int inf = 0x3f3f3f3f;

int n, v, c, d[100][100], readyTime[100], dueDate[100], demand[100], currentDistance, ans=inf, visited[100], timeService[100];
vector<int> vehicle[100];
vector<int> route[100];

void InOut() {
    #define TASK "test"
    freopen(TASK ".txt", "r", stdin);
    freopen(TASK ".out", "w", stdout);
}

bool check (int customerCandidate, int vehicleCandidate) {
    // Nêu đã thăm thành phó trả về 0
    if (visited[customerCandidate] == 1)
        return 0;

    int weight = 0;
    int currentTime = 0;

    for (int i=1; i<vehicle[vehicleCandidate].size(); ++i) {
        int customer = vehicle[vehicleCandidate][i];
        int prevCustomer = vehicle[vehicleCandidate][i-1];
        currentTime += d[customer][prevCustomer];
        if (currentTime < readyTime[customer]) currentTime = readyTime[customer];
        currentTime += timeService[customer];
    }

    // Kiểm tra ràng buộc khối lượng
    if (weight + demand[customerCandidate] > c)
        return 0;

    // Kiểm tra ràng buộc thời gian
    if (currentTime + d[customerCandidate][vehicle[vehicleCandidate].back()] > dueDate[customerCandidate])
        return 0;

    // Thỏa mãn tất cả các điều kiện
    return 1;
}

void Try (int k) {
    // Duyệt qua tập ứng cử viên: n thành phố, mỗi thành phố chọn 1 xe phục vụ
    for (int customerCandidate=1; customerCandidate<=n; ++customerCandidate) {
        for (int vehicleCandidate=1; vehicleCandidate<=v; ++vehicleCandidate) {

            // Kiểm tra ràng buộc về thời gian , khối lương và thành phố đã đia qua chưa
            if (check(customerCandidate, vehicleCandidate) == 1) {
                // Đánh dấu là đã thăm
                visited[customerCandidate] = 1;

                // Lưu tổng quãng đường di chuyển hiện tại
                currentDistance += d[customerCandidate][vehicle[vehicleCandidate].back()];
                // Đẩy ứng cử viên thành phố vào vector ứng cử viên xe
                vehicle[vehicleCandidate].push_back(customerCandidate);

                // Nếu đã duyệt qua hết thành phố
                if (k == n) {
                    int tmp = 0;

                    // cộng thêm hoảng cách về kho
                    for (int k=1; k<=v; ++k) {
                        tmp += d[vehicle[k].back()][0];
                    }
                    tmp += currentDistance;

                    // Cập nhật giá trị kết quả
                    if (ans > tmp) {
                        ans = tmp;
                        for (int t=1; t<=v; ++t) {
                            route[t].clear();
                            for(auto s : vehicle[t]) route[t].push_back(s);
                            route[t].push_back(0);
                        }
                    }
                }
                else {
                    if (currentDistance < ans)
                        Try(k+1);
                }

                // Khôi phục thành phố đã xét
                currentDistance -= d[customerCandidate][vehicle[vehicleCandidate].back()];
                visited[customerCandidate] = 0;
                vehicle[vehicleCandidate].pop_back();
            }
        }
    }
}

void Solve() {
    // Nhập dữ liệu
    cin >> n >> v >> c;
    for (int i=0; i<=n; ++i)
        for (int j=0; j<=n; ++j) cin >> d[i][j];

    for (int i=1; i<=n; ++i) cin >> demand[i];
    for (int i=1; i<=n; ++i) cin >> readyTime[i];
    for (int i=1; i<=n; ++i) cin >> dueDate[i];
    for (int i=1; i<=n; ++i) cin >> timeService[i];

    // Khởi tạo các xe bắt đầu đi từ điểm 0
    for (int i=1; i<=v; ++i) vehicle[i].push_back(0);

    // Backtrack tìm lời giải
    Try(1);

    cout << "weight" << ": " << ans << '\n';

    for (int i=1; i<=v; ++i) {
        cout << "Route " << i << ": ";
        for (auto j : route[i]) cout << j << " ";
        cout << '\n';
    }

}

int main() {
    InOut();
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    Solve();
    return 0;
}
