---
title: SharpDevelop的AddInTree View 插件
date: '2004-10-15 09:25:35 +0800'
---

# 2004-10-15  SharpDevelop的AddInTree View 插件

自从SharpDevelop 源码分析的系列文章发出来之后，很多朋友给了不错的评价，在这里先感谢各位朋友的鼓励。另外，评论中有位朋友想看看我在文章中提到的AddInTreeView插件，其实这个是个很简单的小东西，因此单独发在这里了。\(好像没有找到那里能上传文件，因此直接贴代码了\)

## AddinTreeViewCommand.cs

```text
/*
 * Created by SharpDevelop.
 * User: Administrator
 * Date: 2004-10-4
 * Time: 4:12
 *
 * To change this template use Tools | Options | Coding | Edit Standard Headers.
 */
using System;
using System.Windows.Forms;
using System.CodeDom.Compiler; 

using ICSharpCode.SharpDevelop.Gui;
using ICSharpCode.SharpDevelop.Gui.Pads;
using ICSharpCode.Core.AddIns;
using ICSharpCode.Core.AddIns.Codons;
using ICSharpCode.SharpDevelop.Services; 

namespace Addins.AddinTreeView
{
    /// <summary>
    /// Description of MyClass.
    /// </summary>
    public class AddinTreeViewCommand: AbstractMenuCommand
    {
        public override void Run()
        {
            using (AddinTreeViewContent viewContent = new AddinTreeViewContent() )
            {
                WorkbenchSingleton.Workbench.ShowView(viewContent);
            }
        }
    } 

    public class AddinTreeViewContent: AbstractViewContent
    {
        AddinTreeViewControl viewControl = new AddinTreeViewControl(); 

        public override Control Control
        {
            get
            {
                return viewControl;
            }
        } 

        public override bool IsDirty
        {
            get
            {
                return false;
            }
            set
            {
            }
        } 

        IWorkbenchWindow workbenchWindow;
        public override IWorkbenchWindow WorkbenchWindow
        {
            get
            {
                return workbenchWindow;
            }
            set
            {
                workbenchWindow = value;
                workbenchWindow.Title = "AddInTreeView";
            }
        } 

        public AddinTreeViewContent()
        {
            TitleName = "AddinTree View";
        } 

        public override bool IsViewOnly
        {
            get
            {
                return true;
            }
        }
        public void SaveFile(){}
        public void Undo(){}
        public void Redo(){}
        public override void Save(){}
        public override void Save(string filename){}
        public override void Load(string filename)
        {
        } 

        public override string TabPageText
        {
            get
            {
                return "AddInTree";
            }
        } 

    }
} 
```

## AddinTreeViewControl.cs \#

```text
using System;
using System.Collections;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Windows.Forms; 

using ICSharpCode.SharpDevelop.Gui;
using ICSharpCode.Core.AddIns;
using ICSharpCode.Core.AddIns.Codons; 

namespace Addins.AddinTreeView
{
    /// <summary>
    /// AddinTreeViewControl 的摘要说明。
    /// </summary>
    public class AddinTreeViewControl : System.Windows.Forms.UserControl
    {
        private System.Windows.Forms.ColumnHeader chName;
        private System.Windows.Forms.ListView lvAddin;
        private System.Windows.Forms.ColumnHeader chInfo;
        private System.Windows.Forms.CheckBox cbShowAddinInfo;
        private System.Windows.Forms.Splitter splitter2;
        private System.Windows.Forms.ListView lvDebug;
        private System.Windows.Forms.Splitter splitter1;
        private System.Windows.Forms.TreeView tvAddin;
        private System.Windows.Forms.ColumnHeader chValue;
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.Container components = null; 

        public AddinTreeViewControl()
        {
            // 该调用是 Windows.Forms 窗体设计器所必需的。
            InitializeComponent(); 

            // TODO: 在 InitializeComponent 调用后添加任何初始化
            InitAddinTreeView();
        } 

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        protected override void Dispose( bool disposing )
        {
            if( disposing )
            {
                if(components != null)
                {
                    components.Dispose();
                }
            }
            base.Dispose( disposing );
        } 

        组件设计器生成的代码 

        void InitAddinTreeView()
        {
            TreeNode pathNode = tvAddin.Nodes.Add("AddinRoot"); 

            tvAddin.BeginUpdate();
            try
            {
                foreach ( AddIn addIn in AddInTreeSingleton.AddInTree.AddIns)
                {
                    foreach ( ICSharpCode.Core.AddIns.AddIn.Extension e in addIn.Extensions)
                    {
                        string [] paths = e.Path.Split('/');
                        pathNode = tvAddin.Nodes[0]; 

                        for ( int i=0; i<paths.Length; i++)
                        {
                            bool foundPath = false; 

                            if ( paths[i] == "" )
                            {
                                pathNode = tvAddin.Nodes[0];
                                continue;
                            }                         

                            for ( int j=0; j<pathNode.Nodes.Count; j++)
                            {
                                if ( pathNode.Nodes[j].Text == paths[i] )
                                {
                                    pathNode = pathNode.Nodes[j];
                                    foundPath = true;
                                    break;
                                }
                            } 

                            if ( !foundPath )
                            {
                                pathNode = pathNode.Nodes.Add( paths[i] );
                                pathNode.Tag = new ArrayList();
                                //lvDebug.Items.Add("Add " + e.Path + " ---- " + paths[i]);
                            }
                        } 

                        (pathNode.Tag as ArrayList).Add(e);
                    }
                }
            }
            finally
            {
                tvAddin.EndUpdate();
            }
        } 

        void AddInfo(string Name, string Value)
        {
            lvAddin.Items.Add(Name).SubItems.Add(Value);
        } 

        private void tvAddin_AfterSelect(object sender, System.Windows.Forms.TreeViewEventArgs e)
        {
            lvAddin.Items.Clear(); 

            if ( e.Node.Tag != null )
            {
                foreach (AddIn.Extension et in (e.Node.Tag as ArrayList))
                {
                    AddInfo("Extension", et.ToString()); 

                    foreach ( ICodon codon in et.CodonCollection)
                    {
                        AddInfo("  ┏ Codon ID", codon.ID);
                        AddInfo("  ┣ Codon Name", codon.Name);
                        AddInfo("  ┗ Codon Class", codon.Class); 

                        if ( cbShowAddinInfo.Checked )
                        {
                            AddInfo("      ┣ Addin Name", codon.AddIn.Name);
                            AddInfo("      ┗ Addin FileName", codon.AddIn.FileName); 

                            foreach ( ICSharpCode.Core.AddIns.AddIn.Extension ex in codon.AddIn.Extensions)
                            {
                                AddInfo("          ┣ Addin Extensions", ex.Path);
                            }
                            AddInfo("          ┗━━━━━━━━━", "");
                        }
                    }
                }
            }
        }
    }
} 
```

