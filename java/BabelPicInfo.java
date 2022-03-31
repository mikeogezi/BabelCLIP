import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;
import java.util.TreeSet;
import java.util.List;
import java.util.Map;
import java.util.stream.Collector;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import it.uniroma1.lcl.jlt.util.UniversalPOS;
import it.uniroma1.lcl.jlt.wordnet.WordNetVersion;

import com.google.common.collect.Multimap;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import it.uniroma1.lcl.babelnet.BabelNet;
import it.uniroma1.lcl.babelnet.BabelNetQuery;
import it.uniroma1.lcl.babelnet.BabelNetUtils;
import it.uniroma1.lcl.babelnet.BabelSense;
import it.uniroma1.lcl.babelnet.BabelSenseComparator;
import it.uniroma1.lcl.babelnet.BabelSynset;
import it.uniroma1.lcl.babelnet.BabelSynsetComparator;
import it.uniroma1.lcl.babelnet.BabelSynsetID;
import it.uniroma1.lcl.babelnet.BabelSynsetRelation;
import it.uniroma1.lcl.babelnet.InvalidSynsetIDException;
import it.uniroma1.lcl.babelnet.data.BabelGloss;
import it.uniroma1.lcl.babelnet.data.BabelImage;
import it.uniroma1.lcl.babelnet.data.BabelSenseSource;
import it.uniroma1.lcl.babelnet.impl.BabelNetIndexImageField;
import it.uniroma1.lcl.jlt.util.Language;
import it.uniroma1.lcl.jlt.util.ScoredItem;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;

public class BabelPicInfo {
    public static void main(String[] args) throws IOException, JSONException {
        final File imagesDir = new File("../babelpic-gold/images");
        final File outPath = new File("../gold_synsets.json");
        
        final List<String> bnIds = Files.list(imagesDir.toPath())
            .map(pth -> pth.getFileName().toString().split("_")[0])
            .distinct()
            .sorted()
            .collect(Collectors.toList());
        final Map<String, JSONArray> idToPathMap = new HashMap<>();
        Files.list(imagesDir.toPath()).sorted().forEach(pth -> {
            String name = pth.getFileName().toString();
            String id = name.split("_")[0];
            if (idToPathMap.containsKey(id)) {
                idToPathMap.get(id).put(name);
            } else {
                idToPathMap.put(id, new JSONArray(List.of(name)));
            }
        });
        
        final BabelNet bn = BabelNet.getInstance();
        final JSONArray root = new JSONArray();
        for (String bnId: bnIds) {
            BabelSynset syn = bn.getSynset(new BabelSynsetID(bnId));
            JSONObject synRoot = new JSONObject();

            synRoot.put("id", bnId);
            synRoot.put("images", syn.getImages().stream().map(bi -> {
                final JSONObject imgRoot = new JSONObject();
                try {
                    imgRoot.put("url", bi.getURL());
                    imgRoot.put("body", bi.getName());
                } catch (Exception e) {
                    e.printStackTrace();
                }
                return imgRoot;
            }).collect(Collectors.toList()));
            synRoot.put("goldImages", idToPathMap.get(bnId));
            synRoot.put("lemmas", syn.getLemmas(Language.EN).stream().map(bl -> bl.getLemma()).collect(Collectors.toList()));
            synRoot.put("mainGloss", syn.getMainGloss().isPresent() 
                ? syn.getMainGloss().get().getGloss() 
                : null);
            synRoot.put("mainExample", syn.getMainExample().isPresent() 
                ? syn.getMainExample().get().getExample() 
                : null);
            synRoot.put("mainImage", syn.getMainImage().map(bi -> {
                final JSONObject imgRoot = new JSONObject();
                try {
                    imgRoot.put("url", bi.getURL());
                    imgRoot.put("body", bi.getName());
                } catch (Exception e) {
                    e.printStackTrace();
                }
                return imgRoot;
            }).orElse(null));
            synRoot.put("wn", syn.getWordNetOffsets().stream()
                .filter(wn -> !wn.getVersion().equals(WordNetVersion.WN_30))
                .map(wn -> wn.getID())
                .collect(Collectors.toList()));
            
            root.put(synRoot);
        }

        final FileWriter fw = new FileWriter(outPath);
        fw.write(root.toString(2));
        fw.close();
    }
}
