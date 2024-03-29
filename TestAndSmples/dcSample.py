if __name__ == '__main__':
    def profeelA(name, age, male):
        print(name, age, male)


    def profeelB(name: str, age: int, male: bool):
        print(name, age, male)


    def main():
        profeelA('seki', 60, True)
        profeelB(name='seki', male=True, age=18)
        pass


    main()

    '''
    「自ら定義した関数に引数を追加 → 呼び出し側を修正して動作確認 → OK!」
    
    Happyな瞬間である。がこれを幾度か繰り返すうちに、呼ばれる側の引数リストも呼び出し側の行も膨れていく。
    そして遂にはカオス。あなたにも経験があるだろう。
    


    ITバブル前夜、はじめてのPHPやJavaScriptに抵抗を感じなかったのはその文法・書式がCライクだったから。
    
    「連想配列」には感動した。
    
    
    「オブジェクト指向」
    
    この言葉が流行ったのは80年代末、Cがアセンブラに代わってソフトウェアの開発言語のスタンダードとなって間もない頃のこと。
    この頃のCは「高機能なマクロアセンブラ」なレベルでしかなく、開発者にはCPUのアーキテクチャと周辺機器とのI/Oに対して高い技術的
    スキルを要求される、敷居の高いものだった。その敷居を少しでも下げ、ソフトウェアの生産性を向上させることこそが喫緊の課題とされた
    時代のキーワード、それこそが「オブジェクト指向」である。だがその概念はさておき、成果としてのそれは未だ曖昧模糊としている。
    
    
    
            
    
    
    '''
