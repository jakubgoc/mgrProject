using System.Diagnostics;
using System.IO;
using System.Windows;

namespace OscilloscopeReader
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        string filePath = string.Empty;

        public MainWindow()
        {
            InitializeComponent();
        }

        private void ChooseFileButtonClick(object sender, RoutedEventArgs e)
        {
            Microsoft.Win32.OpenFileDialog openFileDialog = new Microsoft.Win32.OpenFileDialog();

            openFileDialog.InitialDirectory = "::{20D04FE0-3AEA-1069-A2D8-08002B30309D}"; //"D:\\dev\\pythonProject\\hysteresisSimulation\\dist\\main";
            openFileDialog.Filter = "txt files (*.txt)|*.txt|All files (*.*)|*.*";
            openFileDialog.FilterIndex = 2;
            openFileDialog.RestoreDirectory = true;

            bool? resultBool = openFileDialog.ShowDialog();
            if (resultBool == true)
            {
                string filename = openFileDialog.FileName;
                result.Content = filename.ToString();
                filePath = filename.ToString();
            }
        }

        private void PlotArctang(object sender, RoutedEventArgs e)
        {
            string filename = Path.Combine("E:\\dev\\mgr\\OscilloscopeReader\\main.exe");
            var proc = Process.Start(filename, filePath + " plotArctan");
        }

        private void PlotHysteresis(object sender, RoutedEventArgs e)
        {
            string filename = Path.Combine("E:\\dev\\mgr\\OscilloscopeReader\\main.exe");
            var proc = Process.Start(filename, filePath + " plotHysteresis");
        }

        private void CalculateHysteresisArea(object sender, RoutedEventArgs e)
        {
            string filename = Path.Combine("E:\\dev\\mgr\\OscilloscopeReader\\main.exe");
            var proc = Process.Start(filename, filePath + " calculateHysteresisArea");
        }
    }
}
