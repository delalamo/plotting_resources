import os
os.environ.setdefault('MPLBACKEND','Agg')
import tempfile
from pathlib import Path
import unittest
import numpy as np
import matplotlib.pyplot as plt
import plotting_resources as plots


class PlottingResourcesTests(unittest.TestCase):
    def tearDown(self):
        plt.close('all')

    def test_long_captions_preserve_data_and_axes_height(self):
        f,axes=plots.figure();ax=axes[0,0]
        values=np.array([2.,8.,5.]);line=plots.line(ax,[0,1,2],values,'Observed values')
        ax.set(xlabel='Input',ylabel='Response');f.canvas.draw();height=ax.bbox.height/f.dpi
        plots.finish(f,title='A long heading that must wrap without shrinking the font or changing the observations in the plot',
            source='Source: '+('A detailed source credit. '*12),notes='Notes: '+('A detailed explanation of uncertainty. '*12))
        f.canvas.draw()
        np.testing.assert_array_equal(line.get_ydata(),values)
        self.assertAlmostEqual(ax.bbox.height/f.dpi,height)
        self.assertAlmostEqual(f.get_figwidth(),6.75)
        self.assertEqual(f._paper_layout['top_padding_pt'],f._paper_layout['bottom_padding_pt'])
        with tempfile.TemporaryDirectory() as folder:
            outputs=plots.export(f,Path(folder)/'wrapped')
            self.assertTrue(all(p.stat().st_size>0 for p in outputs.values()))

    def test_minimal_removes_captions_and_whitens_background_fills(self):
        f,axes=plots.figure();ax=axes[0,0]
        line=plots.line(ax,[0,1],[2,3],'Observed')
        ax.set(xlabel='Input',ylabel='Response')
        plots.panel_title(ax,'Panel title','A')
        annotation=ax.text(.2,.5,'Annotation',transform=ax.transAxes,
                           bbox=dict(facecolor=plots.STYLE['panel']))
        plots.finish(f,title='REMOVE TITLE',subtitle='REMOVE SUBTITLE',
                     source='REMOVE SOURCE',notes='REMOVE NOTES',minimal=True)
        self.assertEqual(f.texts,[])
        self.assertIsNone(f._paper_layout['footer_top_pt'])
        self.assertEqual(f.get_facecolor(),(1,1,1,1))
        self.assertEqual(ax.get_facecolor(),(1,1,1,1))
        self.assertEqual(annotation.get_bbox_patch().get_facecolor(),(1,1,1,1))
        self.assertEqual(line.get_markerfacecolor(),'white')
        self.assertEqual(line.get_color(),plots.BLUE)
        self.assertEqual(ax.get_xlabel(),'Input')
        self.assertEqual(ax.get_title(loc='left'),'Panel title')
        self.assertEqual(f.legends[0].get_texts()[0].get_text(),'Observed')

    def test_multi_panel_defaults_to_text_width(self):
        f,axes=plots.figure(2,2,sharex=True,sharey=True)
        plots.finish(f,title='Shared panels')
        self.assertAlmostEqual(f.get_figwidth()*72,486)
        self.assertEqual(len(axes.flat),4)

    def test_focus_is_last_and_references_are_opaque(self):
        f,axes=plots.figure();ax=axes[0,0]
        focus=[2,3,4];references={'A':[1,2,3],'B':[4,5,6]}
        plots.emphasis_lines(ax,[0,1,2],focus,references)
        self.assertEqual(ax.lines[-1].get_color(),plots.BLUE)
        np.testing.assert_array_equal(ax.lines[-1].get_ydata(),focus)
        for line,values in zip(ax.lines[:-1],references.values()):
            self.assertEqual(line.get_alpha(),1)
            np.testing.assert_array_equal(line.get_ydata(),values)

    def test_stacks_do_not_renormalize_source_rounding(self):
        f,axes=plots.figure()
        totals=plots.stacked_bars(axes[0,0],['A','B'],{'First':[.4,.6],'Second':[.599,.401]})
        np.testing.assert_allclose(totals,[.999,1.001])


if __name__=='__main__':unittest.main()
