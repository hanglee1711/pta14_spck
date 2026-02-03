from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QIcon, QColor, QPen, QPainterPath, QFont


class Icons:
    """Clean, modern vector icons drawn with QPainter."""

    @staticmethod
    def _pen(color, width=2.0):
        pen = QPen(color, width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        return pen

    @staticmethod
    def _create_dual(draw_fn, size=24):
        icon = QIcon()
        for color, state in [(QColor("#64748B"), QIcon.State.Off),
                              (QColor("#FFFFFF"), QIcon.State.On)]:
            px = QPixmap(size, size)
            px.fill(Qt.GlobalColor.transparent)
            p = QPainter(px)
            p.setRenderHint(QPainter.RenderHint.Antialiasing)
            draw_fn(p, size, color)
            p.end()
            icon.addPixmap(px, QIcon.Mode.Normal, state)
        return icon

    @staticmethod
    def _create_single(draw_fn, size=24, color="#EF4444"):
        px = QPixmap(size, size)
        px.fill(Qt.GlobalColor.transparent)
        p = QPainter(px)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        draw_fn(p, size, QColor(color))
        p.end()
        return QIcon(px)

    # ── Individual icon draw functions ─────────────────────

    @staticmethod
    def _draw_home(p, s, c):
        p.setPen(Icons._pen(c))
        p.setBrush(Qt.BrushStyle.NoBrush)
        path = QPainterPath()
        path.moveTo(s * 0.12, s * 0.48)
        path.lineTo(s * 0.5, s * 0.1)
        path.lineTo(s * 0.88, s * 0.48)
        p.drawPath(path)
        p.drawRoundedRect(QRectF(s * 0.22, s * 0.47, s * 0.56, s * 0.42), 3, 3)
        p.drawRoundedRect(QRectF(s * 0.4, s * 0.6, s * 0.2, s * 0.29), 2, 2)

    @staticmethod
    def _draw_exam(p, s, c):
        p.setPen(Icons._pen(c))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(QRectF(s * 0.18, s * 0.08, s * 0.64, s * 0.84), 4, 4)
        p.drawLine(QPointF(s * 0.32, s * 0.35), QPointF(s * 0.68, s * 0.35))
        p.drawLine(QPointF(s * 0.32, s * 0.50), QPointF(s * 0.68, s * 0.50))
        p.drawLine(QPointF(s * 0.32, s * 0.65), QPointF(s * 0.58, s * 0.65))
        path = QPainterPath()
        path.moveTo(s * 0.28, s * 0.22)
        path.lineTo(s * 0.38, s * 0.28)
        path.lineTo(s * 0.50, s * 0.14)
        p.drawPath(path)

    @staticmethod
    def _draw_calendar(p, s, c):
        p.setPen(Icons._pen(c))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(QRectF(s * 0.1, s * 0.18, s * 0.8, s * 0.72), 4, 4)
        p.drawLine(QPointF(s * 0.1, s * 0.40), QPointF(s * 0.9, s * 0.40))
        p.drawLine(QPointF(s * 0.30, s * 0.08), QPointF(s * 0.30, s * 0.28))
        p.drawLine(QPointF(s * 0.70, s * 0.08), QPointF(s * 0.70, s * 0.28))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(c)
        r = s * 0.045
        for row in range(2):
            for col in range(3):
                cx = s * 0.28 + col * s * 0.20
                cy = s * 0.53 + row * s * 0.18
                p.drawEllipse(QPointF(cx, cy), r, r)

    @staticmethod
    def _draw_bell(p, s, c):
        p.setPen(Icons._pen(c))
        p.setBrush(Qt.BrushStyle.NoBrush)
        path = QPainterPath()
        path.moveTo(s * 0.18, s * 0.62)
        path.cubicTo(s * 0.18, s * 0.32, s * 0.30, s * 0.14, s * 0.50, s * 0.14)
        path.cubicTo(s * 0.70, s * 0.14, s * 0.82, s * 0.32, s * 0.82, s * 0.62)
        p.drawPath(path)
        p.drawLine(QPointF(s * 0.12, s * 0.65), QPointF(s * 0.88, s * 0.65))
        p.drawLine(QPointF(s * 0.50, s * 0.06), QPointF(s * 0.50, s * 0.14))
        arc = QPainterPath()
        arc.moveTo(s * 0.38, s * 0.70)
        arc.cubicTo(s * 0.38, s * 0.88, s * 0.62, s * 0.88, s * 0.62, s * 0.70)
        p.drawPath(arc)

    @staticmethod
    def _draw_logout(p, s, c):
        p.setPen(Icons._pen(c))
        p.setBrush(Qt.BrushStyle.NoBrush)
        path = QPainterPath()
        path.moveTo(s * 0.52, s * 0.15)
        path.lineTo(s * 0.22, s * 0.15)
        path.lineTo(s * 0.22, s * 0.85)
        path.lineTo(s * 0.52, s * 0.85)
        p.drawPath(path)
        p.drawLine(QPointF(s * 0.42, s * 0.50), QPointF(s * 0.85, s * 0.50))
        arrow = QPainterPath()
        arrow.moveTo(s * 0.70, s * 0.36)
        arrow.lineTo(s * 0.85, s * 0.50)
        arrow.lineTo(s * 0.70, s * 0.64)
        p.drawPath(arrow)

    @staticmethod
    def _draw_person(p, s, c):
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(255, 255, 255, 50))
        p.drawEllipse(1, 1, s - 2, s - 2)
        p.setBrush(QColor(255, 255, 255, 180))
        head_r = s * 0.17
        p.drawEllipse(QPointF(s * 0.5, s * 0.33), head_r, head_r)
        body = QPainterPath()
        body.moveTo(s * 0.18, s * 0.88)
        body.cubicTo(s * 0.18, s * 0.58, s * 0.32, s * 0.54, s * 0.50, s * 0.54)
        body.cubicTo(s * 0.68, s * 0.54, s * 0.82, s * 0.58, s * 0.82, s * 0.88)
        body.closeSubpath()
        p.drawPath(body)

    # ── Public API ─────────────────────────────────────────

    @staticmethod
    def home(size=24):
        return Icons._create_dual(Icons._draw_home, size)

    @staticmethod
    def exam(size=24):
        return Icons._create_dual(Icons._draw_exam, size)

    @staticmethod
    def calendar(size=24):
        return Icons._create_dual(Icons._draw_calendar, size)

    @staticmethod
    def bell(size=24):
        return Icons._create_dual(Icons._draw_bell, size)

    @staticmethod
    def logout(size=24):
        return Icons._create_single(Icons._draw_logout, size, "#EF4444")

    @staticmethod
    def person_avatar(size=72):
        px = QPixmap(size, size)
        px.fill(Qt.GlobalColor.transparent)
        p = QPainter(px)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        Icons._draw_person(p, size, QColor("white"))
        p.end()
        return px
