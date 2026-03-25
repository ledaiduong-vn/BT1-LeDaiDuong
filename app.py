import os
from typing import Optional
from urllib.parse import quote

import streamlit as st
from PIL import Image


APP_TITLE = "Denergy - Thi công lắp đặt điện mặt trời"
DEFAULT_COMPANY_NAME = "Denergy"
DEFAULT_SLOGAN = "Công ty thi công, lắp đặt điện mặt trời"
DESTINATION_EMAIL = "denergylamdong@gmail.com"

LOGO_FILENAME = "Annotation 2026-03-25 194156.png"

HERO_IMAGE_FILENAME = "hero_flower_solar_wind.png"

def _hero_image_path() -> str:
    """
    Trả về đường dẫn ảnh hero.

    Lưu ý: ảnh hero có thể nằm trong nhiều vị trí khác nhau (tuỳ môi trường Cursor),
    nên ta thử nhiều candidate path để app luôn tìm thấy ảnh.
    """
    candidates: list[str] = []

    # 1) Nếu bạn tự copy vào thư mục assets của project.
    candidates.append(os.path.join(os.path.dirname(__file__), "assets", HERO_IMAGE_FILENAME))

    # 2) Nếu ảnh nằm ngay trong thư mục project.
    candidates.append(os.path.join(os.path.dirname(__file__), HERO_IMAGE_FILENAME))

    # 3) Thử trong thư mục Cursor projects (hiện tại công cụ đã tạo ảnh ở đây).
    cursor_projects_root = os.path.join(os.path.expanduser("~"), ".cursor", "projects")
    try:
        if os.path.isdir(cursor_projects_root):
            for folder in os.listdir(cursor_projects_root):
                assets_path = os.path.join(cursor_projects_root, folder, "assets", HERO_IMAGE_FILENAME)
                candidates.append(assets_path)
    except Exception:
        # Nếu không truy cập được thư mục, bỏ qua.
        pass

    for p in candidates:
        if os.path.exists(p):
            return p

    # Không tìm thấy, trả về path theo candidate đầu tiên để load_hero_image() kiểm tra tồn tại.
    return candidates[0] if candidates else os.path.join(os.path.dirname(__file__), "assets", HERO_IMAGE_FILENAME)


def _logo_path() -> str:
    return os.path.join(os.path.dirname(__file__), LOGO_FILENAME)


@st.cache_data(show_spinner=False)
def load_logo() -> Optional[Image.Image]:
    path = _logo_path()
    if not os.path.exists(path):
        return None
    # PIL Image is used by st.image
    return Image.open(path)


def load_hero_image() -> Optional[Image.Image]:
    path = _hero_image_path()
    if not os.path.exists(path):
        return None
    return Image.open(path)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .page-wrap {
          max-width: 1100px;
          margin-left: auto;
          margin-right: auto;
        }
        .hero {
          border: 1px solid rgba(0,0,0,0.06);
          border-radius: 16px;
          padding: 18px 18px;
          background: linear-gradient(180deg, rgba(0,123,255,0.10), rgba(0,0,0,0));
        }
        .card {
          border: 1px solid rgba(0,0,0,0.06);
          border-radius: 14px;
          padding: 14px;
          background: white;
          box-shadow: 0 6px 18px rgba(0,0,0,0.04);
          height: 100%;
        }
        .card-title {
          font-weight: 800;
          margin-top: 6px;
          margin-bottom: 8px;
        }
        .muted { color: rgba(0,0,0,0.62); }
        .small { font-size: 0.95rem; }
        .pill {
          display: inline-block;
          padding: 6px 10px;
          border-radius: 999px;
          background: rgba(0, 123, 255, 0.10);
          border: 1px solid rgba(0, 123, 255, 0.20);
          color: #0056b3;
          font-weight: 700;
          margin-right: 8px;
          margin-bottom: 8px;
        }
        .section-title {
          font-size: 1.35rem;
          font-weight: 900;
          margin: 6px 0 12px 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="⚡", layout="wide")
    inject_styles()

    logo = load_logo()
    hero = load_hero_image()

    if logo:
        st.sidebar.image(logo, use_container_width=True)
    st.sidebar.title("Tùy chọn nhanh")

    company_name = st.sidebar.text_input(
        "Tên công ty",
        value=DEFAULT_COMPANY_NAME,
        help="Bạn có thể thay đổi tên hiển thị trên website.",
    )
    slogan = st.sidebar.text_input(
        "Slogan",
        value=DEFAULT_SLOGAN,
        help="Dòng mô tả ngắn phía trên trang.",
    )

    nav = st.sidebar.radio(
        "Đi tới",
        ["Giới thiệu", "Dịch vụ", "Dự án tiêu biểu", "Quy trình thi công", "Liên hệ"],
        index=0,
    )

    st.title(company_name)
    st.markdown(f"<div class='muted small'>{slogan}</div>", unsafe_allow_html=True)

    if hero:
        st.image(hero, use_container_width=True)

    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)

    if nav == "Giới thiệu":
        render_intro(logo)
    elif nav == "Dịch vụ":
        render_services()
    elif nav == "Dự án tiêu biểu":
        render_projects()
    elif nav == "Quy trình thi công":
        render_process()
    else:
        render_contact()

    st.markdown("</div>", unsafe_allow_html=True)


def render_intro(logo: Optional[Image.Image]) -> None:
    st.markdown("<div class='hero'>", unsafe_allow_html=True)
    cols = st.columns([1.1, 1])
    with cols[0]:
        st.markdown("<div class='section-title'>Giải pháp điện mặt trời trọn gói</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <p class='muted small'>
            Chúng tôi tư vấn - thiết kế - thi công - lắp đặt hệ thống điện mặt trời cho nhà ở và doanh nghiệp.
            Cam kết tối ưu hiệu suất, thi công an toàn và bảo hành minh bạch.
            </p>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div class='pill'>Tư vấn miễn phí</div>", unsafe_allow_html=True)
        st.markdown("<div class='pill'>Thi công đúng tiến độ</div>", unsafe_allow_html=True)
        st.markdown("<div class='pill'>Bảo hành rõ ràng</div>", unsafe_allow_html=True)

    with cols[1]:
        if logo:
            st.image(logo, use_container_width=True)
        else:
            st.info("Không tìm thấy logo. Vui lòng kiểm tra file ảnh trong thư mục dự án.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Vì sao chọn chúng tôi")
    c2 = st.columns(3)
    cards = [
        ("Thiết kế tối ưu", "Tính toán sản lượng, bố trí hệ thống phù hợp công suất và điều kiện thực tế."),
        ("Thi công chuyên nghiệp", "Kết cấu chắc chắn, đi dây gọn gàng, quy trình an toàn rõ ràng."),
        ("Hỗ trợ sau lắp đặt", "Hướng dẫn vận hành, theo dõi hiệu quả và hỗ trợ bảo hành khi cần."),
    ]
    for i, (title, desc) in enumerate(cards):
        with c2[i]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-title'>{title}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='muted small'>{desc}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


def render_services() -> None:
    st.markdown("### Các dịch vụ chính")
    services = [
        ("Khảo sát & tư vấn", "Đánh giá mặt bằng, nhu cầu điện, đề xuất cấu hình tối ưu."),
        ("Thiết kế hệ thống", "Bố trí tấm pin, inverter, dây dẫn và tính toán sản lượng dự kiến."),
        ("Thi công lắp đặt", "Lên khung, bắt tấm, đi dây, đấu nối và kiểm tra nghiệm thu."),
        ("Vận hành & bảo hành", "Hướng dẫn sử dụng, kiểm tra định kỳ và hỗ trợ kỹ thuật."),
    ]

    cols = st.columns(2)
    for idx, (title, desc) in enumerate(services):
        with cols[idx % 2]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-title'>{title}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='muted small'>{desc}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


def render_projects() -> None:
    st.markdown("### Dự án tiêu biểu")
    st.markdown(
        "<div class='muted small'>Tải ảnh dự án lên và thêm ghi chú riêng cho từng tấm ảnh.</div>",
        unsafe_allow_html=True,
    )

    uploaded_files = st.file_uploader(
        "Upload hình ảnh dự án",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
        key="project_upload",
    )

    if uploaded_files:
        st.markdown("#### Ảnh bạn đã tải lên")
        grid = st.columns(3)

        for i, uf in enumerate(uploaded_files):
            title = os.path.splitext(os.path.basename(uf.name))[0]
            note_key = f"project_note_{i}_{uf.name}"

            with grid[i % 3]:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.image(uf, use_container_width=True)
                st.markdown(f"<div class='card-title'>{title}</div>", unsafe_allow_html=True)
                st.text_area(
                    "Ghi chú",
                    value=st.session_state.get(note_key, ""),
                    key=note_key,
                    height=120,
                )
                st.markdown("</div>", unsafe_allow_html=True)

        st.caption("Ghi chú được lưu tạm trong phiên làm việc (session).")
    else:
        sample_projects = [
            ("Nhà dân 5kWp", "Lắp đặt mái tôn, hệ inverter 5kWp, tối ưu bố trí theo hướng nắng."),
            ("Nhà xưởng 20kWp", "Khung thép chắc chắn, hệ thống quản lý theo dõi sản lượng."),
            ("Công trình thương mại 50kWp", "Tổng hợp nhiều dãy pin, quy trình nghiệm thu đầy đủ."),
            ("Trang trại nông nghiệp", "Tận dụng diện tích mái chuồng, giảm chi phí vận hành dài hạn."),
            ("Văn phòng kết hợp nhà ở", "Thi công gọn gàng, đảm bảo thẩm mỹ và an toàn điện."),
            ("Khu dịch vụ - nhà hàng", "Thiết kế theo tải thực tế, hướng dẫn vận hành rõ ràng."),
        ]

        grid = st.columns(3)
        for i, (title, desc) in enumerate(sample_projects):
            with grid[i % 3]:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='card-title'>{title}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='muted small'>{desc}</div>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='muted small' style='margin-top:10px;'>"
                    "Tải ảnh dự án thật lên và thêm ghi chú cho từng tấm.</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)


def render_process() -> None:
    st.markdown("### Quy trình thi công chuẩn")
    steps = [
        ("01. Liên hệ & khảo sát", "Tiếp nhận nhu cầu, trao đổi thông số và khảo sát thực tế."),
        ("02. Tư vấn cấu hình", "Đề xuất cấu hình tấm pin/inverter, dự kiến sản lượng và phương án thi công."),
        ("03. Thiết kế & báo giá", "Chốt bản thiết kế, báo giá minh bạch và lịch thi công dự kiến."),
        ("04. Thi công lắp đặt", "Lắp khung, bắt tấm, đi dây, đấu nối, kiểm tra an toàn."),
        ("05. Nghiệm thu & bàn giao", "Kiểm tra hoạt động, lập biên bản nghiệm thu và hướng dẫn vận hành."),
        ("06. Bảo hành & hỗ trợ", "Theo dõi hiệu quả, hỗ trợ kỹ thuật và bảo hành khi cần."),
    ]

    cols = st.columns(2)
    for i, (title, desc) in enumerate(steps):
        with cols[i % 2]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-title'>{title}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='muted small'>{desc}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


def render_contact() -> None:
    st.markdown("### Liên hệ báo giá")
    st.markdown(
        "<div class='muted small'>Điền thông tin bên dưới. Chúng tôi sẽ phản hồi trong thời gian sớm nhất.</div>",
        unsafe_allow_html=True,
    )

    with st.form("contact_form", clear_on_submit=False):
        name = st.text_input("Họ và tên", placeholder="Ví dụ: Nguyễn Văn A")
        phone = st.text_input("Số điện thoại", placeholder="Ví dụ: 0901xxxxxx")
        email = st.text_input("Email (tuỳ chọn)", placeholder="name@email.com")
        address = st.text_input("Địa chỉ (tuỳ chọn)", placeholder="Ví dụ: Quận/Huyện, Tỉnh/TP")
        capacity = st.selectbox(
            "Công suất dự kiến (tuỳ chọn)",
            ["Chưa xác định", "3-5kWp", "5-10kWp", "10-30kWp", "30-100kWp", "Khác"],
            index=0,
        )
        message = st.text_area("Nội dung yêu cầu", placeholder="Mô tả nhu cầu lắp đặt...")

        submitted = st.form_submit_button("Gửi yêu cầu")

    if submitted:
        phone_digits = "".join(ch for ch in phone if ch.isdigit())
        if not name.strip():
            st.error("Vui lòng nhập họ và tên.")
            return
        if len(phone_digits) < 8:
            st.error("Số điện thoại chưa hợp lệ. Vui lòng kiểm tra lại.")
            return
        if not message.strip():
            st.error("Vui lòng nhập nội dung yêu cầu.")
            return

        st.success("Cảm ơn bạn! Yêu cầu của bạn đã được ghi nhận (demo).")
        st.markdown("### Thông tin bạn đã nhập")
        st.write(
            {
                "Họ tên": name,
                "Số điện thoại": phone,
                "Email": email if email.strip() else None,
                "Địa chỉ": address if address.strip() else None,
                "Công suất dự kiến": capacity,
                "Nội dung": message,
            }
        )

        # Tạo liên kết mailto để mở ứng dụng email và tự điền nội dung.
        subject = f"Yêu cầu báo giá điện mặt trời - {name}"
        body = (
            f"Họ tên: {name}\n"
            f"Số điện thoại: {phone}\n"
            f"Email: {email if email.strip() else '-'}\n"
            f"Địa chỉ: {address if address.strip() else '-'}\n"
            f"Công suất dự kiến: {capacity}\n"
            f"Nội dung: {message}\n"
        )
        mailto_link = (
            f"mailto:{DESTINATION_EMAIL}"
            f"?subject={quote(subject)}"
            f"&body={quote(body)}"
        )
        st.info("Bạn có thể bấm vào link dưới đây để gửi email (mở ứng dụng email của bạn).")
        st.markdown(
            f"[Gửi email tới {DESTINATION_EMAIL}]({mailto_link})",
        )


if __name__ == "__main__":
    main()

