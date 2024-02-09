"""Evaluation metrics that will be used to assess the output of the trained model compared
to references codes."""

from typing import Tuple, List, Any
from Levenshtein import distance
from datasets import load_metric
from nltk.translate.bleu_score import sentence_bleu


class EM:
    """
    Evaluation metrics that will be used to assess the output of the trained model compared
    to reference codes.
    """

    def __init__(self) -> None:
        """
        Initializes an instance of the EM class.
        """
        pass

    def edit_distance(self, generated_code: str, reference_code: str) -> int:
        """
        Computes the Levenshtein edit distance between the generated code and the reference code.

        Parameters:
            generated_code: A string representing the generated code.
            reference_code: A string representing the reference code.

        Returns:
            The Levenshtein edit distance between the two input strings.
        """
        return distance(generated_code, reference_code)

    def bleu(
        self,
        generated_code: List[str],
        reference_code: List[str],
        weights: Tuple[int, int, int, int],
    ):
        """
        Computes the BLEU score between the generated code and the reference code.

        Parameters:
            generated_code: A list of strings representing the generated code.
            reference_code: A list of strings representing the reference code.
            weights: A tuple of integers representing the weights for the BLEU score computation.

        Returns:
            The BLEU score between the generated and reference code based on the specified weights.
        """
        return sentence_bleu([reference_code], generated_code, weights)

    def rouge(self, reference_code: str, generated_code: str):
        """
        Computes the ROUGE score between the generated code and the reference code using the ROUGE metric.

        Parameters:
            reference_code: A string representing the reference code.
            generated_code: A string representing the generated code.

        Returns:
            A dictionary for the ROUGE score, which can be access using output['rouge1'], output['rouge2'],
            output['rougeL'], output['rougeLsum']
        """
        rouge = load_metric("rouge")
        return rouge.compute(generated_code, reference_code)
