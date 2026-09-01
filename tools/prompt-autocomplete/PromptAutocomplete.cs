using System;
using System.Collections.Generic;
using System.Drawing;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text.RegularExpressions;
using System.Text;
using System.Threading;
using System.Windows.Automation;
using System.Windows.Forms;

namespace AgentPromptAutocomplete
{
    internal static class NativeMethods
    {
        internal const int WH_KEYBOARD_LL = 13;
        internal const int WM_KEYDOWN = 0x0100;
        internal const int WM_SYSKEYDOWN = 0x0104;

        internal delegate IntPtr KeyboardProc(int code, IntPtr wParam, IntPtr lParam);

        [DllImport("user32.dll")]
        internal static extern IntPtr GetForegroundWindow();

        [DllImport("user32.dll")]
        internal static extern bool SetForegroundWindow(IntPtr window);

        [DllImport("user32.dll")]
        internal static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);

        [DllImport("user32.dll", CharSet = CharSet.Unicode)]
        internal static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);

        [DllImport("user32.dll")]
        internal static extern bool GetCaretPos(out Point point);

        [DllImport("user32.dll")]
        internal static extern bool ClientToScreen(IntPtr hWnd, ref Point point);

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern IntPtr SetWindowsHookEx(int hook, KeyboardProc callback, IntPtr module, uint threadId);

        [DllImport("user32.dll", SetLastError = true)]
        internal static extern bool UnhookWindowsHookEx(IntPtr hook);

        [DllImport("user32.dll")]
        internal static extern IntPtr CallNextHookEx(IntPtr hook, int code, IntPtr wParam, IntPtr lParam);

        [DllImport("kernel32.dll", CharSet = CharSet.Unicode)]
        internal static extern IntPtr GetModuleHandle(string moduleName);

        [DllImport("gdi32.dll")]
        internal static extern IntPtr CreateRoundRectRgn(int left, int top, int right, int bottom, int width, int height);

        [DllImport("gdi32.dll")]
        internal static extern bool DeleteObject(IntPtr handle);

        [DllImport("user32.dll")]
        internal static extern void keybd_event(byte virtualKey, byte scanCode, uint flags, UIntPtr extraInfo);

        [DllImport("user32.dll")]
        internal static extern short GetAsyncKeyState(int virtualKey);

        [DllImport("user32.dll")]
        internal static extern bool SetProcessDpiAwarenessContext(IntPtr value);

        [DllImport("user32.dll")]
        internal static extern IntPtr SetThreadDpiAwarenessContext(IntPtr value);

        [DllImport("user32.dll")]
        internal static extern uint GetDpiForWindow(IntPtr window);
    }

    internal sealed class KeyboardHook : IDisposable
    {
        private readonly NativeMethods.KeyboardProc callback;
        private readonly Func<Keys, bool> keyHandler;
        private IntPtr handle;

        internal KeyboardHook(Func<Keys, bool> handler)
        {
            keyHandler = handler;
            callback = HookCallback;
            handle = NativeMethods.SetWindowsHookEx(
                NativeMethods.WH_KEYBOARD_LL,
                callback,
                NativeMethods.GetModuleHandle(null),
                0);
            if (handle == IntPtr.Zero) throw new InvalidOperationException("Unable to install keyboard hook.");
        }

        private IntPtr HookCallback(int code, IntPtr wParam, IntPtr lParam)
        {
            if (code >= 0 && (wParam.ToInt32() == NativeMethods.WM_KEYDOWN || wParam.ToInt32() == NativeMethods.WM_SYSKEYDOWN))
            {
                int virtualKey = Marshal.ReadInt32(lParam);
                if (keyHandler((Keys)virtualKey)) return new IntPtr(1);
            }
            return NativeMethods.CallNextHookEx(handle, code, wParam, lParam);
        }

        public void Dispose()
        {
            if (handle == IntPtr.Zero) return;
            NativeMethods.UnhookWindowsHookEx(handle);
            handle = IntPtr.Zero;
        }
    }

    internal sealed class PromptItem
    {
        internal string Text { get; set; }
        internal string Scope { get; set; }
        internal string Group { get; set; }
        public override string ToString() { return Text; }
    }

    internal sealed class PromptPaletteMetrics : IDisposable
    {
        internal const int BaselineDpi = 96;
        internal readonly int Dpi;
        internal readonly int PreferredWidth;
        internal readonly int MinimumWidth;
        internal readonly int ScreenMargin;
        internal readonly int HeaderHeight;
        internal readonly int FooterHeight;
        internal readonly int ContentInset;
        internal readonly int RowPaddingTop;
        internal readonly int RowPaddingBottom;
        internal readonly int TitleDescriptionGap;
        internal readonly int ScrollbarWidth;
        internal readonly int ScrollbarHitWidth;
        internal readonly int ScrollbarMargin;
        internal readonly int MinimumThumbHeight;
        internal readonly int SelectionMarkerWidth;
        internal readonly int CornerRadius;
        internal readonly int PopupGap;
        internal readonly int BorderWidth;
        internal readonly int TitleHeight;
        internal readonly int DescriptionHeight;
        internal readonly int RowHeight;
        internal readonly Font TitleFont;
        internal readonly Font DescriptionFont;
        internal readonly Font HeaderFont;
        internal readonly Font FooterFont;

        internal PromptPaletteMetrics(int dpi)
        {
            Dpi = Math.Max(BaselineDpi, dpi);
            PreferredWidth = Scale(760);
            MinimumWidth = Scale(360);
            ScreenMargin = Scale(12);
            HeaderHeight = Scale(42);
            FooterHeight = Scale(34);
            ContentInset = Scale(12);
            RowPaddingTop = Scale(7);
            RowPaddingBottom = Scale(7);
            TitleDescriptionGap = Scale(2);
            ScrollbarWidth = Math.Max(Scale(6), 4);
            ScrollbarHitWidth = Math.Max(Scale(20), ScrollbarWidth + Scale(10));
            ScrollbarMargin = Scale(6);
            MinimumThumbHeight = Scale(36);
            SelectionMarkerWidth = Math.Max(Scale(3), 2);
            CornerRadius = Scale(12);
            PopupGap = Scale(6);
            BorderWidth = Math.Max(Scale(1), 1);

            TitleFont = PixelFont("Segoe UI", 15, FontStyle.Regular);
            DescriptionFont = PixelFont("Segoe UI", 11, FontStyle.Regular);
            HeaderFont = PixelFont("Segoe UI Semibold", 11, FontStyle.Bold);
            FooterFont = PixelFont("Segoe UI", 11, FontStyle.Regular);
            TitleHeight = MeasureLine(TitleFont);
            DescriptionHeight = MeasureLine(DescriptionFont);
            RowHeight = RowPaddingTop + TitleHeight + TitleDescriptionGap + DescriptionHeight + RowPaddingBottom;
        }

        internal int Scale(int logical)
        {
            return Math.Max(1, (int)Math.Round(logical * (Dpi / (double)BaselineDpi)));
        }

        private Font PixelFont(string family, int logicalPixels, FontStyle style)
        {
            return new Font(family, Scale(logicalPixels), style, GraphicsUnit.Pixel);
        }

        private static int MeasureLine(Font font)
        {
            return TextRenderer.MeasureText("AgÁỹ", font, Size.Empty,
                TextFormatFlags.NoPadding | TextFormatFlags.SingleLine).Height;
        }

        internal int ChromeHeight { get { return (BorderWidth * 2) + HeaderHeight + FooterHeight; } }

        public void Dispose()
        {
            TitleFont.Dispose();
            DescriptionFont.Dispose();
            HeaderFont.Dispose();
            FooterFont.Dispose();
        }
    }

    internal sealed class PromptPaletteLayout
    {
        internal Rectangle Bounds;
        internal int VisibleRows;
        internal bool OpensBelow;

        internal static PromptPaletteLayout Calculate(Rectangle workingArea, Rectangle anchor, PromptPaletteMetrics metrics, int itemCount)
        {
            int leftLimit = workingArea.Left + metrics.ScreenMargin;
            int rightLimit = workingArea.Right - metrics.ScreenMargin;
            int topLimit = workingArea.Top + metrics.ScreenMargin;
            int bottomLimit = workingArea.Bottom - metrics.ScreenMargin;
            int availableWidth = Math.Max(1, rightLimit - leftLimit);
            int width = Math.Min(metrics.PreferredWidth, availableWidth);
            if (availableWidth >= metrics.MinimumWidth) width = Math.Max(metrics.MinimumWidth, width);

            int desiredRows = Math.Max(1, Math.Min(5, itemCount));
            int belowTop = anchor.Bottom + metrics.PopupGap;
            int aboveBottom = anchor.Top - metrics.PopupGap;
            int belowSpace = Math.Max(0, bottomLimit - belowTop);
            int aboveSpace = Math.Max(0, aboveBottom - topLimit);
            int desiredHeight = metrics.ChromeHeight + (desiredRows * metrics.RowHeight);
            bool opensBelow = belowSpace >= desiredHeight || belowSpace >= aboveSpace;
            int chosenSpace = opensBelow ? belowSpace : aboveSpace;
            int rowsThatFit = (chosenSpace - metrics.ChromeHeight) / metrics.RowHeight;
            int visibleRows = Math.Max(1, Math.Min(desiredRows, rowsThatFit));
            int height = metrics.ChromeHeight + (visibleRows * metrics.RowHeight);
            height = Math.Min(height, Math.Max(1, bottomLimit - topLimit));

            int x = Math.Max(leftLimit, Math.Min(anchor.Left, rightLimit - width));
            int y = opensBelow ? belowTop : aboveBottom - height;
            y = Math.Max(topLimit, Math.Min(y, bottomLimit - height));

            return new PromptPaletteLayout
            {
                Bounds = new Rectangle(x, y, width, height),
                VisibleRows = visibleRows,
                OpensBelow = opensBelow
            };
        }
    }

    internal sealed class PromptListControl : Control
    {
        private readonly List<PromptItem> items = new List<PromptItem>();
        private PromptPaletteMetrics metrics;
        private int selectedIndex;
        private int scrollOffset;
        private bool draggingScrollbar;
        private int dragStartY;
        private int dragStartOffset;
        internal event Action DoubleClicked;

        internal PromptListControl()
        {
            SetStyle(ControlStyles.AllPaintingInWmPaint | ControlStyles.OptimizedDoubleBuffer |
                ControlStyles.ResizeRedraw | ControlStyles.UserPaint, true);
            BackColor = Color.FromArgb(23, 25, 28);
            TabStop = false;
        }

        internal void ApplyMetrics(PromptPaletteMetrics value)
        {
            metrics = value;
            EnsureVisible();
            Invalidate();
        }

        internal void SetItems(IEnumerable<PromptItem> source)
        {
            string previous = SelectedText;
            items.Clear();
            items.AddRange(source);
            selectedIndex = previous == null ? 0 : items.FindIndex(item => item.Text == previous);
            if (selectedIndex < 0) selectedIndex = 0;
            scrollOffset = 0;
            EnsureVisible();
            Invalidate();
        }

        internal void MoveSelection(int delta)
        {
            if (items.Count == 0) return;
            selectedIndex = Math.Max(0, Math.Min(items.Count - 1, selectedIndex + delta));
            EnsureVisible();
            Invalidate();
        }

        internal string SelectedText
        {
            get { return selectedIndex >= 0 && selectedIndex < items.Count ? items[selectedIndex].Text : null; }
        }

        private int VisibleRows { get { return metrics == null ? 1 : Math.Max(1, Height / metrics.RowHeight); } }

        private void EnsureVisible()
        {
            if (selectedIndex < scrollOffset) scrollOffset = selectedIndex;
            if (selectedIndex >= scrollOffset + VisibleRows) scrollOffset = selectedIndex - VisibleRows + 1;
            scrollOffset = Math.Max(0, Math.Min(Math.Max(0, items.Count - VisibleRows), scrollOffset));
        }

        protected override void OnMouseMove(MouseEventArgs args)
        {
            base.OnMouseMove(args);
            if (draggingScrollbar)
            {
                if (metrics == null) return;
                int maxOffset = Math.Max(0, items.Count - VisibleRows);
                Rectangle track;
                Rectangle thumb;
                GetScrollbarGeometry(out track, out thumb);
                int trackHeight = track.Height;
                int thumbHeight = thumb.Height;
                int travel = Math.Max(1, trackHeight - thumbHeight);
                int offsetDelta = ((args.Y - dragStartY) * Math.Max(1, maxOffset)) / travel;
                scrollOffset = Math.Max(0, Math.Min(maxOffset, dragStartOffset + offsetDelta));
                Invalidate();
                return;
            }
            int index = metrics == null ? -1 : scrollOffset + (args.Y / metrics.RowHeight);
            if (index >= 0 && index < items.Count && index != selectedIndex)
            {
                selectedIndex = index;
                Invalidate();
            }
        }

        protected override void OnMouseDown(MouseEventArgs args)
        {
            base.OnMouseDown(args);
            if (metrics != null && args.Button == MouseButtons.Left &&
                args.X >= Width - metrics.ScrollbarHitWidth && items.Count > VisibleRows)
            {
                draggingScrollbar = true;
                dragStartY = args.Y;
                dragStartOffset = scrollOffset;
                Capture = true;
            }
        }

        protected override void OnMouseUp(MouseEventArgs args)
        {
            base.OnMouseUp(args);
            draggingScrollbar = false;
            Capture = false;
        }

        protected override void OnMouseWheel(MouseEventArgs args)
        {
            base.OnMouseWheel(args);
            int direction = args.Delta > 0 ? -2 : 2;
            scrollOffset = Math.Max(0, Math.Min(Math.Max(0, items.Count - VisibleRows), scrollOffset + direction));
            Invalidate();
        }

        protected override void OnMouseDoubleClick(MouseEventArgs args)
        {
            base.OnMouseDoubleClick(args);
            if (metrics != null && args.X < Width - metrics.ScrollbarHitWidth && DoubleClicked != null) DoubleClicked();
        }

        protected override void OnPaint(PaintEventArgs args)
        {
            base.OnPaint(args);
            args.Graphics.Clear(BackColor);
            if (metrics == null) return;
            args.Graphics.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;

            int rows = Math.Min(VisibleRows, items.Count - scrollOffset);
            for (int visibleIndex = 0; visibleIndex < rows; visibleIndex++)
            {
                int itemIndex = scrollOffset + visibleIndex;
                PromptItem item = items[itemIndex];
                Rectangle rowBounds = new Rectangle(0, visibleIndex * metrics.RowHeight, Width, metrics.RowHeight);
                Rectangle row = new Rectangle(metrics.BorderWidth, rowBounds.Top + metrics.BorderWidth,
                    Math.Max(1, Width - metrics.ScrollbarHitWidth - (metrics.BorderWidth * 2)),
                    Math.Max(1, metrics.RowHeight - (metrics.BorderWidth * 2)));
                bool selected = itemIndex == selectedIndex;
                if (selected)
                {
                    using (SolidBrush selection = new SolidBrush(Color.FromArgb(31, 52, 53)))
                        args.Graphics.FillRectangle(selection, row);
                    using (SolidBrush marker = new SolidBrush(Color.FromArgb(20, 184, 166)))
                        args.Graphics.FillRectangle(marker, row.Left,
                            row.Top + metrics.RowPaddingTop,
                            metrics.SelectionMarkerWidth,
                            Math.Max(1, row.Height - metrics.RowPaddingTop - metrics.RowPaddingBottom));
                }

                int textLeft = row.Left + metrics.ContentInset;
                int textWidth = Math.Max(1, row.Right - metrics.ContentInset - textLeft);
                int titleTop = rowBounds.Top + metrics.RowPaddingTop;
                Rectangle titleRect = new Rectangle(textLeft, titleTop, textWidth, metrics.TitleHeight);
                int descriptionTop = titleRect.Bottom + metrics.TitleDescriptionGap;
                Rectangle descriptionRect = new Rectangle(textLeft, descriptionTop, textWidth, metrics.DescriptionHeight);

                Region previousClip = args.Graphics.Clip;
                args.Graphics.SetClip(rowBounds);
                TextRenderer.DrawText(args.Graphics, item.Text, metrics.TitleFont, titleRect,
                    selected ? Color.White : Color.FromArgb(235, 238, 242),
                    TextFormatFlags.Left | TextFormatFlags.SingleLine | TextFormatFlags.EndEllipsis | TextFormatFlags.NoPrefix | TextFormatFlags.NoPadding);
                string description = item.Group + "  •  " + (item.Scope == "BridgeChat" ? "BridgeChat workflow" : "Shared workflow");
                TextRenderer.DrawText(args.Graphics, description, metrics.DescriptionFont, descriptionRect,
                    Color.FromArgb(157, 168, 178),
                    TextFormatFlags.Left | TextFormatFlags.SingleLine | TextFormatFlags.EndEllipsis | TextFormatFlags.NoPrefix | TextFormatFlags.NoPadding);
                args.Graphics.Clip = previousClip;
                previousClip.Dispose();
            }

            DrawScrollbar(args.Graphics);
        }

        private void DrawScrollbar(Graphics graphics)
        {
            if (items.Count <= VisibleRows) return;
            Rectangle track;
            Rectangle thumb;
            GetScrollbarGeometry(out track, out thumb);
            using (SolidBrush trackBrush = new SolidBrush(Color.FromArgb(43, 47, 52)))
                FillCapsule(graphics, trackBrush, track.X, track.Y, track.Width, track.Height);
            using (SolidBrush thumbBrush = new SolidBrush(draggingScrollbar ? Color.FromArgb(20, 184, 166) : Color.FromArgb(100, 110, 120)))
            {
                FillCapsule(graphics, thumbBrush, thumb.X, thumb.Y, thumb.Width, thumb.Height);
            }
        }

        private void GetScrollbarGeometry(out Rectangle track, out Rectangle thumb)
        {
            int trackX = Width - metrics.ScrollbarMargin - metrics.ScrollbarWidth;
            int trackHeight = Math.Max(1, Height - (metrics.ScrollbarMargin * 2));
            int thumbHeight = Math.Max(metrics.MinimumThumbHeight,
                (trackHeight * VisibleRows) / Math.Max(1, items.Count));
            thumbHeight = Math.Min(trackHeight, thumbHeight);
            int travel = Math.Max(0, trackHeight - thumbHeight);
            int maxOffset = Math.Max(1, items.Count - VisibleRows);
            int thumbTop = metrics.ScrollbarMargin + ((travel * scrollOffset) / maxOffset);
            track = new Rectangle(trackX, metrics.ScrollbarMargin, metrics.ScrollbarWidth, trackHeight);
            thumb = new Rectangle(trackX, thumbTop, metrics.ScrollbarWidth, thumbHeight);
        }

        private static void FillCapsule(Graphics graphics, Brush brush, int x, int y, int width, int height)
        {
            int radius = width;
            graphics.FillRectangle(brush, x, y + (radius / 2), width, Math.Max(1, height - radius));
            graphics.FillEllipse(brush, x, y, width, radius);
            graphics.FillEllipse(brush, x, y + height - radius, width, radius);
        }

        protected override void Dispose(bool disposing) { base.Dispose(disposing); }
    }

    internal sealed class SuggestionForm : Form
    {
        private readonly PromptListControl list = new PromptListControl();
        private readonly Panel content;
        private readonly Panel header;
        private readonly Panel footer;
        private readonly Label title;
        private readonly Label help;
        private PromptPaletteMetrics metrics;
        internal event Action<string> Accepted;
        internal event Action DpiChangedRequested;

        internal SuggestionForm()
        {
            FormBorderStyle = FormBorderStyle.None;
            AutoScaleMode = AutoScaleMode.None;
            ShowInTaskbar = false;
            TopMost = true;
            StartPosition = FormStartPosition.Manual;
            BackColor = Color.FromArgb(53, 58, 64);
            content = new Panel { Dock = DockStyle.Fill, BackColor = Color.FromArgb(23, 25, 28) };
            header = new Panel { Dock = DockStyle.Top, BackColor = content.BackColor };
            title = new Label
            {
                AutoSize = true,
                Text = "PROMPT PALETTE",
                ForeColor = Color.FromArgb(20, 184, 166)
            };
            header.Controls.Add(title);

            footer = new Panel { Dock = DockStyle.Bottom, BackColor = content.BackColor };
            help = new Label
            {
                Dock = DockStyle.Fill,
                TextAlign = ContentAlignment.MiddleLeft,
                ForeColor = Color.FromArgb(157, 168, 178),
            };
            footer.Controls.Add(help);

            list.Dock = DockStyle.Fill;
            list.DoubleClicked += AcceptCurrent;
            content.Controls.Add(list);
            content.Controls.Add(footer);
            content.Controls.Add(header);
            Controls.Add(content);
        }

        protected override bool ShowWithoutActivation { get { return true; } }
        protected override CreateParams CreateParams
        {
            get
            {
                const int WS_EX_NOACTIVATE = 0x08000000;
                const int CS_DROPSHADOW = 0x00020000;
                CreateParams parameters = base.CreateParams;
                parameters.ExStyle |= WS_EX_NOACTIVATE;
                parameters.ClassStyle |= CS_DROPSHADOW;
                return parameters;
            }
        }

        protected override void OnResize(EventArgs args)
        {
            base.OnResize(args);
            if (metrics == null) return;
            IntPtr rounded = NativeMethods.CreateRoundRectRgn(0, 0, Width + 1, Height + 1,
                metrics.CornerRadius * 2, metrics.CornerRadius * 2);
            Region previous = Region;
            Region = Region.FromHrgn(rounded);
            if (previous != null) previous.Dispose();
            NativeMethods.DeleteObject(rounded);
        }

        protected override void WndProc(ref Message message)
        {
            const int WM_DPICHANGED = 0x02E0;
            base.WndProc(ref message);
            if (message.Msg == WM_DPICHANGED && DpiChangedRequested != null) DpiChangedRequested();
        }

        internal void ApplyLayout(PromptPaletteMetrics value, PromptPaletteLayout layout)
        {
            PromptPaletteMetrics previous = metrics;
            metrics = value;
            SuspendLayout();
            Padding = new Padding(metrics.BorderWidth);
            content.Padding = new Padding(metrics.ContentInset, 0, metrics.ContentInset, 0);
            header.Height = metrics.HeaderHeight;
            footer.Height = metrics.FooterHeight;
            Font previousTitleFont = title.Font;
            Font previousHelpFont = help.Font;
            title.Font = new Font(metrics.HeaderFont.FontFamily, metrics.HeaderFont.Size, metrics.HeaderFont.Style, GraphicsUnit.Pixel);
            help.Font = new Font(metrics.FooterFont.FontFamily, metrics.FooterFont.Size, metrics.FooterFont.Style, GraphicsUnit.Pixel);
            title.Location = new Point(metrics.Scale(4), Math.Max(0, (metrics.HeaderHeight - title.PreferredHeight) / 2));
            help.Padding = new Padding(metrics.Scale(4), 0, 0, 0);
            help.Text = ChooseFooterText(layout.Bounds.Width - (metrics.ContentInset * 2));
            list.ApplyMetrics(metrics);
            Bounds = layout.Bounds;
            ResumeLayout(true);
            if (previous != null)
            {
                previousTitleFont.Dispose();
                previousHelpFont.Dispose();
                previous.Dispose();
            }
        }

        private string ChooseFooterText(int availableWidth)
        {
            string full = "↑↓  Navigate     Tab / Enter  Insert     Esc  Close     Mouse wheel  Scroll";
            string medium = "↑↓  Navigate     Tab / Enter  Insert     Esc  Close";
            string compact = "↑↓  Navigate     Enter  Insert     Esc  Close";
            if (TextRenderer.MeasureText(full, help.Font, Size.Empty, TextFormatFlags.NoPadding).Width <= availableWidth) return full;
            if (TextRenderer.MeasureText(medium, help.Font, Size.Empty, TextFormatFlags.NoPadding).Width <= availableWidth) return medium;
            return compact;
        }

        internal void SetItems(IEnumerable<PromptItem> items)
        {
            list.SetItems(items);
        }

        internal void MoveSelection(int delta) { list.MoveSelection(delta); }
        internal void AcceptCurrent()
        {
            if (SelectedText != null && Accepted != null) Accepted(SelectedText);
        }
        internal string SelectedText { get { return list.SelectedText; } }

        protected override void Dispose(bool disposing)
        {
            if (disposing && metrics != null) metrics.Dispose();
            base.Dispose(disposing);
        }
    }

    internal sealed class AutocompleteContext : ApplicationContext
    {
        private readonly List<PromptItem> prompts;
        private readonly Regex windowPattern;
        private readonly int minimumCharacters;
        private readonly SuggestionForm popup;
        private readonly System.Windows.Forms.Timer timer;
        private readonly KeyboardHook keyboardHook;
        private AutomationElement target;
        private string currentValue = String.Empty;
        private string typedBuffer = String.Empty;
        private string lastRenderKey = String.Empty;
        private string lastLayoutKey = String.Empty;
        private DateTime lastTypedAt = DateTime.MinValue;
        private string pendingSuggestion;
        private IntPtr pendingWindow = IntPtr.Zero;

        internal AutocompleteContext(string catalogPath, string titlePattern, int minimum)
        {
            prompts = LoadPrompts(catalogPath);
            windowPattern = new Regex(titlePattern, RegexOptions.IgnoreCase | RegexOptions.CultureInvariant);
            minimumCharacters = minimum;
            popup = new SuggestionForm();
            popup.Accepted += QueueAccept;
            popup.DpiChangedRequested += delegate { lastLayoutKey = String.Empty; };

            keyboardHook = new KeyboardHook(HandleGlobalKey);
            timer = new System.Windows.Forms.Timer();
            timer.Interval = 180;
            timer.Tick += delegate
            {
                if (pendingSuggestion != null) CommitPendingSuggestion();
                else RefreshSuggestions();
            };
            timer.Start();
        }

        private static List<PromptItem> LoadPrompts(string path)
        {
            List<PromptItem> result = new List<PromptItem>();
            string scope = "Shared";
            string group = "general";
            Regex bullet = new Regex("^\\s*-\\s+[“\"](?<text>.+?)[”\"]\\s*$");
            Regex heading = new Regex("^##\\s+`(?<group>[^`]+)`");
            foreach (string line in File.ReadLines(path))
            {
                if (line.StartsWith("# BridgeChat", StringComparison.OrdinalIgnoreCase)) scope = "BridgeChat";
                if (line.StartsWith("# Automatically chained BridgeChat", StringComparison.OrdinalIgnoreCase)) scope = "BridgeChat";
                Match headingMatch = heading.Match(line);
                if (headingMatch.Success) group = headingMatch.Groups["group"].Value.Trim();
                Match match = bullet.Match(line);
                if (!match.Success) continue;
                string text = match.Groups["text"].Value.Trim();
                if (text.Length > 0 && !result.Any(item => String.Equals(item.Text, text, StringComparison.OrdinalIgnoreCase)))
                    result.Add(new PromptItem { Text = text, Scope = scope, Group = group });
            }
            return result;
        }

        private static string ForegroundIdentity()
        {
            IntPtr window = NativeMethods.GetForegroundWindow();
            var title = new System.Text.StringBuilder(512);
            NativeMethods.GetWindowText(window, title, title.Capacity);
            string processName = String.Empty;
            try
            {
                uint processId;
                NativeMethods.GetWindowThreadProcessId(window, out processId);
                processName = Process.GetProcessById((int)processId).ProcessName;
            }
            catch { }
            return processName + " " + title;
        }

        private void RefreshSuggestions()
        {
            if (!windowPattern.IsMatch(ForegroundIdentity())) { HidePopup(); return; }

            AutomationElement focused;
            try { focused = AutomationElement.FocusedElement; }
            catch { HidePopup(); return; }
            if (focused == null) { HidePopup(); return; }

            string value;
            string fragment = String.Empty;
            if (TryReadText(focused, out value)) fragment = LastLine(value).TrimStart();
            if (fragment.Length < minimumCharacters || !HasMatches(fragment)) fragment = typedBuffer.TrimStart();
            if (NormalizeForSearch(fragment).Length < minimumCharacters) { HidePopup(); return; }

            string normalizedFragment = NormalizeForSearch(fragment).Trim();
            List<PromptItem> groupMatches = prompts
                .Where(item => NormalizeForSearch(item.Group).StartsWith(normalizedFragment, StringComparison.OrdinalIgnoreCase))
                .ToList();
            bool groupMode = groupMatches.Count > 0;
            List<PromptItem> matches = (groupMode ? groupMatches : prompts
                .Where(item => NormalizeForSearch(item.Text).StartsWith(normalizedFragment, StringComparison.OrdinalIgnoreCase)))
                .OrderBy(item => item.Scope == "BridgeChat" ? 1 : 0)
                .ThenBy(item => item.Text.Length)
                .Take(12)
                .ToList();

            if (matches.Count == 0 || (matches.Count == 1 && String.Equals(matches[0].Text, fragment, StringComparison.CurrentCultureIgnoreCase)))
            {
                HidePopup();
                return;
            }

            string renderKey = normalizedFragment + "|" + String.Join("|", matches.Select(item => item.Text));
            if (popup.Visible && String.Equals(lastRenderKey, renderKey, StringComparison.Ordinal))
            {
                PositionPopup(focused, matches.Count);
                return;
            }

            target = focused;
            currentValue = value ?? String.Empty;
            popup.SetItems(matches);
            PositionPopup(focused, matches.Count);
            lastRenderKey = renderKey;
            if (!popup.Visible) popup.Show();
        }

        private static string LastLine(string value)
        {
            int newline = Math.Max(value.LastIndexOf('\n'), value.LastIndexOf('\r'));
            return newline < 0 ? value : value.Substring(newline + 1);
        }

        private static bool TryReadText(AutomationElement element, out string value)
        {
            value = String.Empty;
            try
            {
                object rawPattern;
                if (element.TryGetCurrentPattern(ValuePattern.Pattern, out rawPattern))
                {
                    ValuePattern valuePattern = rawPattern as ValuePattern;
                    if (valuePattern != null)
                    {
                        value = valuePattern.Current.Value ?? String.Empty;
                        return true;
                    }
                }

                if (element.TryGetCurrentPattern(TextPattern.Pattern, out rawPattern))
                {
                    TextPattern textPattern = rawPattern as TextPattern;
                    if (textPattern != null)
                    {
                        value = textPattern.DocumentRange.GetText(-1) ?? String.Empty;
                        return true;
                    }
                }
            }
            catch { }
            return false;
        }

        private bool HasMatches(string fragment)
        {
            string normalized = NormalizeForSearch(fragment);
            return normalized.Length >= minimumCharacters && prompts.Any(
                item => NormalizeForSearch(item.Text).StartsWith(normalized, StringComparison.OrdinalIgnoreCase));
        }

        private static string NormalizeForSearch(string value)
        {
            if (String.IsNullOrWhiteSpace(value)) return String.Empty;
            string decomposed = value.ToLowerInvariant().Normalize(NormalizationForm.FormD);
            var plain = new StringBuilder(decomposed.Length);
            foreach (char character in decomposed)
            {
                System.Globalization.UnicodeCategory category = System.Globalization.CharUnicodeInfo.GetUnicodeCategory(character);
                if (category != System.Globalization.UnicodeCategory.NonSpacingMark) plain.Append(character);
            }
            string result = plain.ToString().Normalize(NormalizationForm.FormC).Replace("\u0111", "d");
            result = Regex.Replace(result, "([aeou])w(?=\\s|$)", "$1");
            result = Regex.Replace(result, "([aeo])\\1", "$1");
            result = Regex.Replace(result, "dd", "d");
            result = Regex.Replace(result, "[fsrxj](?=\\s|$)", String.Empty);
            return Regex.Replace(result, "[-_\\s]+", String.Empty);
        }

        private void PositionPopup(AutomationElement focused, int itemCount)
        {
            PromptPaletteMetrics pendingMetrics = null;
            try
            {
                System.Windows.Rect rect = focused.Current.BoundingRectangle;
                Rectangle anchor = Rectangle.FromLTRB(
                    (int)Math.Floor(rect.Left),
                    (int)Math.Floor(rect.Top),
                    (int)Math.Ceiling(rect.Right),
                    (int)Math.Ceiling(rect.Bottom));
                Screen screen = Screen.FromRectangle(anchor);
                uint rawDpi = NativeMethods.GetDpiForWindow(NativeMethods.GetForegroundWindow());
                int dpi = rawDpi == 0 ? PromptPaletteMetrics.BaselineDpi : (int)rawDpi;
                string layoutKey = dpi + "|" + screen.WorkingArea + "|" + anchor + "|" + itemCount;
                if (String.Equals(lastLayoutKey, layoutKey, StringComparison.Ordinal)) return;
                pendingMetrics = new PromptPaletteMetrics(dpi);
                PromptPaletteLayout layout = PromptPaletteLayout.Calculate(screen.WorkingArea, anchor, pendingMetrics, itemCount);
                popup.ApplyLayout(pendingMetrics, layout);
                pendingMetrics = null;
                lastLayoutKey = layoutKey;
            }
            catch { }
            finally
            {
                if (pendingMetrics != null) pendingMetrics.Dispose();
            }
        }

        private void HidePopup()
        {
            if (popup.Visible) popup.Hide();
            target = null;
            lastRenderKey = String.Empty;
        }

        private void QueueAccept(string suggestion)
        {
            if (String.IsNullOrWhiteSpace(suggestion)) return;
            pendingSuggestion = suggestion;
            pendingWindow = NativeMethods.GetForegroundWindow();
            HidePopup();
            typedBuffer = String.Empty;
        }

        private void CommitPendingSuggestion()
        {
            string suggestion = pendingSuggestion;
            IntPtr targetWindow = pendingWindow;
            pendingSuggestion = null;
            pendingWindow = IntPtr.Zero;
            if (String.IsNullOrWhiteSpace(suggestion) || targetWindow == IntPtr.Zero) return;

            Clipboard.SetText(suggestion, TextDataFormat.UnicodeText);
            NativeMethods.SetForegroundWindow(targetWindow);
            Thread.Sleep(60);
            SendChord((byte)Keys.ControlKey, (byte)Keys.A);
            Thread.Sleep(50);
            SendChord((byte)Keys.ControlKey, (byte)Keys.V);
            typedBuffer = String.Empty;
        }

        private static void SendChord(byte modifier, byte key)
        {
            const uint KEYEVENTF_KEYUP = 0x0002;
            NativeMethods.keybd_event(modifier, 0, 0, UIntPtr.Zero);
            NativeMethods.keybd_event(key, 0, 0, UIntPtr.Zero);
            NativeMethods.keybd_event(key, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
            NativeMethods.keybd_event(modifier, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        }

        private bool HandleGlobalKey(Keys key)
        {
            if (!windowPattern.IsMatch(ForegroundIdentity())) { typedBuffer = String.Empty; return false; }
            if (popup.Visible)
            {
                if (key == Keys.Down) { popup.MoveSelection(1); return true; }
                if (key == Keys.Up) { popup.MoveSelection(-1); return true; }
                if (key == Keys.Tab || key == Keys.Enter)
                {
                    QueueAccept(popup.SelectedText);
                    return true;
                }
                if (key == Keys.Escape) { typedBuffer = String.Empty; HidePopup(); return true; }
            }

            bool controlDown = (NativeMethods.GetAsyncKeyState((int)Keys.ControlKey) & 0x8000) != 0;
            if (controlDown && key == Keys.A)
            {
                typedBuffer = String.Empty;
                lastTypedAt = DateTime.UtcNow;
                HidePopup();
                return false;
            }

            if (key == Keys.Delete)
            {
                typedBuffer = String.Empty;
                lastTypedAt = DateTime.UtcNow;
                HidePopup();
                return false;
            }

            if (DateTime.UtcNow - lastTypedAt > TimeSpan.FromSeconds(4)) typedBuffer = String.Empty;

            if (key >= Keys.A && key <= Keys.Z)
            {
                typedBuffer += ((char)('a' + (key - Keys.A))).ToString();
            }
            else if (key >= Keys.D0 && key <= Keys.D9)
            {
                typedBuffer += ((char)('0' + (key - Keys.D0))).ToString();
            }
            else if (key == Keys.Space)
            {
                typedBuffer += " ";
            }
            else if (key == Keys.OemMinus || key == Keys.Subtract)
            {
                typedBuffer += "-";
            }
            else if (key == Keys.Back && typedBuffer.Length > 0)
            {
                typedBuffer = typedBuffer.Substring(0, typedBuffer.Length - 1);
            }
            else if (key == Keys.Enter)
            {
                typedBuffer = String.Empty;
            }

            if (typedBuffer.Length > 120) typedBuffer = typedBuffer.Substring(typedBuffer.Length - 120);
            lastTypedAt = DateTime.UtcNow;
            return false;
        }

        protected override void ExitThreadCore()
        {
            timer.Stop();
            keyboardHook.Dispose();
            popup.Dispose();
            base.ExitThreadCore();
        }
    }

    public static class Program
    {
        private static void EnablePerMonitorV2()
        {
            IntPtr perMonitorV2 = new IntPtr(-4);
            try { NativeMethods.SetProcessDpiAwarenessContext(perMonitorV2); }
            catch { }
            try { NativeMethods.SetThreadDpiAwarenessContext(perMonitorV2); }
            catch { }
        }

        public static string ValidateLayoutMatrix()
        {
            int[,] resolutions = new int[,]
            {
                { 1366, 768 }, { 1600, 900 }, { 1920, 1080 }, { 2560, 1440 }, { 3840, 2160 }
            };
            int[] dpis = new int[] { 96, 120, 144, 168, 192, 240 };
            int[] itemCounts = new int[] { 1, 2, 5, 12 };
            int cases = 0;
            for (int resolutionIndex = 0; resolutionIndex < resolutions.GetLength(0); resolutionIndex++)
            {
                for (int dpiIndex = 0; dpiIndex < dpis.Length; dpiIndex++)
                {
                    using (PromptPaletteMetrics metrics = new PromptPaletteMetrics(dpis[dpiIndex]))
                    {
                        if (metrics.RowPaddingTop + metrics.TitleHeight >=
                            metrics.RowPaddingTop + metrics.TitleHeight + metrics.TitleDescriptionGap)
                            throw new InvalidOperationException("Typography invariant failed: title and description overlap.");
                        int descriptionBottom = metrics.RowPaddingTop + metrics.TitleHeight +
                            metrics.TitleDescriptionGap + metrics.DescriptionHeight;
                        if (descriptionBottom > metrics.RowHeight - metrics.RowPaddingBottom)
                            throw new InvalidOperationException("Typography invariant failed: description exceeds row.");

                        int width = resolutions[resolutionIndex, 0];
                        int height = resolutions[resolutionIndex, 1] - 48;
                        Rectangle[] workingAreas = new Rectangle[]
                        {
                            new Rectangle(0, 0, width, height),
                            new Rectangle(-width, -120, width, height)
                        };
                        foreach (Rectangle work in workingAreas)
                        {
                            Rectangle[] anchors = new Rectangle[]
                            {
                                new Rectangle(work.Left + (work.Width / 2), work.Top + (work.Height / 2), 320, 48),
                                new Rectangle(work.Right - 180, work.Bottom - 72, 160, 48),
                                new Rectangle(work.Left + 20, work.Top + 20, 280, 48)
                            };
                            foreach (Rectangle anchor in anchors)
                            {
                                foreach (int itemCount in itemCounts)
                                {
                                    PromptPaletteLayout layout = PromptPaletteLayout.Calculate(work, anchor, metrics, itemCount);
                                    Rectangle safe = Rectangle.FromLTRB(
                                        work.Left + metrics.ScreenMargin,
                                        work.Top + metrics.ScreenMargin,
                                        work.Right - metrics.ScreenMargin,
                                        work.Bottom - metrics.ScreenMargin);
                                    if (layout.Bounds.Left < safe.Left || layout.Bounds.Top < safe.Top ||
                                        layout.Bounds.Right > safe.Right || layout.Bounds.Bottom > safe.Bottom)
                                        throw new InvalidOperationException("Responsive invariant failed: popup escaped WorkingArea.");
                                    if (layout.VisibleRows < 1 || layout.VisibleRows > Math.Min(5, itemCount))
                                        throw new InvalidOperationException("Responsive invariant failed: invalid visible row count.");
                                    int expectedHeight = metrics.ChromeHeight + (layout.VisibleRows * metrics.RowHeight);
                                    if (layout.Bounds.Height != expectedHeight)
                                        throw new InvalidOperationException("Layout invariant failed: header/list/footer height mismatch.");
                                    cases++;
                                }
                            }
                        }
                    }
                }
            }
            return "Prompt palette layout matrix: PASS (" + cases + " cases)";
        }

        [STAThread]
        public static void Run(string catalogPath, string titlePattern, int minimumCharacters)
        {
            EnablePerMonitorV2();
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new AutocompleteContext(catalogPath, titlePattern, minimumCharacters));
        }
    }
}
