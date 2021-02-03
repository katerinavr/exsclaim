import unittest
import json
import pathlib
import os
import shutil

import responses
from deepdiff import DeepDiff

from ..pipeline import Pipeline
from ..tool import JournalScraper, CaptionDistributor
from ..figure import FigureSeparator

class TestNatureFull(unittest.TestCase):

    def setUp(self):
        """ Instantiates a test search query and Exsclaim pipeline to test """
        # Set paths
        current_directory = pathlib.Path(__file__).resolve(strict=True)
        self.test_directory = current_directory.parent
        self.data = self.test_directory / "data"
        query_path = self.data / 'nature_test.json'

        # Initialize EXSCLAIM! pipeline
        self.exsclaim_pipeline = Pipeline(query_path)

        # Expected results
        expected_json = self.data / "nature_closed_expected.json"
        with open(expected_json, "r") as f:
          self.expected = json.load(f)

    def tearDown(self):
        shutil.rmtree(self.exsclaim_pipeline.query_dict["results_dir"])

    @responses.activate
    def test_full_run(self):
        """ tests one full run of pipeline """
        expected = self.expected        
        ##  Set up Mock URLs
        # For HTML Files
        test_articles = self.data / 'nature_articles'
        for article_name in os.listdir(test_articles):
            url = ("https://www.nature.com/articles/"
                   + article_name.split(".")[0])
            with open(test_articles / article_name, "r") as f:
                article_html = f.read()
            responses.add(responses.GET, url, body = article_html)
        search_url_1 = ("https://www.nature.com/search?q=%22Ag+nanoparticle"
                        "%22%20%22HAADF-STEM%22&order=relevance&page=1")
        search_url_2 = ("https://www.nature.com/search?q=%22Ag+nanoparticle"
                        "%22%20%22HAADF+STEM%22&order=relevance&page=1")
        test_search = self.data / 'nature_search.html'
        with open(test_search, "r") as f:
            article_html = f.read()
        responses.add(responses.GET, search_url_1, body = article_html)
        responses.add(responses.GET, search_url_2, body = article_html)
        # For images
        images = self.data / "images" / "pipeline"
        for image in expected:
            url = expected[image]["image_url"]
            image_path = images / image
            if not os.path.isfile(image_path):
                continue
            with open(image_path, "rb") as f:
                responses.add(
                    responses.GET,
                    url,
                    body = f.read(),
                    status = 200,
                    content_type = "img/jpg",
                    stream = True
                )

        # Run the tools through the pipeline
        exsclaim_json = self.exsclaim_pipeline.run()

        # Test for basic validity of result exsclaim json
        self.assertEqual(len(exsclaim_json), 14,
            ("Expected result EXSCLAIM JSON to contain 14 Figure JSONs. "
             "Result had {} Figure JSONs".format(len(exsclaim_json))))
        for figure_name in exsclaim_json:
            figure_json = exsclaim_json[figure_name]
            self.assertEqual(figure_name, figure_json["figure_name"])
            if figure_json["article_name"] == "s41467-018-06211-3":
                self.assertTrue(figure_json["open"])

        # Run comparison of expected and resulting jsons
        diff = DeepDiff(expected, exsclaim_json, ignore_order=True,
                        significant_digits=1,
                        ignore_numeric_type_changes=True)

        ## Band-aid to handle https://github.com/MaterialEyes/exsclaim/issues/5
        ## in testing. This will call the test a pass if we find either of the 
        ## results that appear seemingly nondeterministically. 
        accepted_difference = {'values_changed': {"root['s41467-018-06211-3_fig2.jpg']['master_images'][4]['caption'][0]": {'new_value': 'f, g', 'old_value': 'Corresponding ABF intensity profiles of the white box in d present the peaks of the silver and manganese atomic columns'}}, 'iterable_item_removed': {"root['s41467-018-06211-3_fig2.jpg']['master_images'][4]['general'][0]": 'ABF-STEM', "root['s41467-018-06211-3_fig2.jpg']['master_images'][4]['general'][1]": 'Intensity profile'}}
        success = (diff in ({}, accepted_difference))
        self.assertTrue(success,
            ("The resulting json and the reference json are different. This "
             "does not mean the implementation is incorrect, just that a "
              "change has been made to the code that changes results. If you "
              "have made a change that you believe improves results, you "
              "should use other methods to check correctness and accuracy. "
              "The diff of the result and extpected is: {}".format(diff)))


if __name__ == '__main__':
    unittest.main()