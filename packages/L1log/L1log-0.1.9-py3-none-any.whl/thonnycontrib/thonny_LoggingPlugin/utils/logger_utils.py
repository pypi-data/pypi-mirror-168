import re 

def sans_commentaire_entete(s : str) -> str:
    '''Renvoie une chaîne identique à `s` mais sans les premiers
    commentaires et autres lignes blanches.

    Au cas où l'éditeur soit vide
    >>> sans_commentaire_entete('')
    ''
    
    Uniquement un en-tête
    >>> s = "\\n#sdf\\n#qsdfgt\\n#sdfghjk\\n\\t#qsdfgh\\n"
    >>> sans_commentaire_entete(s)
    ''

    Pas d'en-tête
    >>> s = "def toto():\\n\\treturn"
    >>> sans_commentaire_entete(s)
    'def toto():\\n\\treturn'
    

    Des commentaires et espacement avant un début de programme
    >>> s = "# nom prenom\\n\\n  # nom prenom\\n\\t  \\n# pouet pouet\\ndef toto():\\n\\treturn"
    >>> sans_commentaire_entete(s)
    'def toto():\\n\\treturn'
    '''
    liste_lignes = re.split('\n', s)
    i = 0
    while i < len(liste_lignes) and (liste_lignes[i].strip() == '' or liste_lignes[i].strip()[0] == '#'):
        i = i + 1
    return '\n'.join(liste_lignes[i:])    

def cut_topfile_comments(s : str) -> str:
    """
    cut the header of the file where the program begins
    """
    if not isinstance(s,str):
        return s
    return sans_commentaire_entete(s)

def cut_filename(s : str) -> str:
        """
        Cut the filename to keep only the last part, that is the name
        without the access path.

        Args : 
            s (str) the filename

        Return :
            (str) the filename cutted

        """
        try :
            return re.search("\/[^\/]*$",s).group()
        except Exception as e :
            return s

def hash_filename(s : str) -> str:
    """
    Returns a hashed name for s : its hash value.
    """
    return "file_" + str(s.__hash__()) 

import doctest
if __name__ == '__main__':
    doctest.testmod(verbose=True)
