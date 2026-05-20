window.BENCHMARK_DATA = {
  "lastUpdate": 1779300973747,
  "repoUrl": "https://github.com/nikolasil/chronicle-mcp",
  "entries": {
    "Python Benchmark": [
      {
        "commit": {
          "author": {
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "id": "89344ee2dc736c40cce36a49be24274bc9122b6d",
          "message": "Refactor/service layer",
          "timestamp": "2026-02-12T22:16:20Z",
          "url": "https://github.com/nikolasil/chronicle-mcp/pull/7/commits/89344ee2dc736c40cce36a49be24274bc9122b6d"
        },
        "date": 1771007450064,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 202997.33120407932,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017560946983814427",
            "extra": "mean: 4.926173137688544 usec\nrounds: 16149"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 206040.18947180183,
            "unit": "iter/sec",
            "range": "stddev: 7.525074787073789e-7",
            "extra": "mean: 4.853422055976403 usec\nrounds: 35827"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 202891.97657641274,
            "unit": "iter/sec",
            "range": "stddev: 7.617671230165135e-7",
            "extra": "mean: 4.92873112517282 usec\nrounds: 36954"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 298405.47058101237,
            "unit": "iter/sec",
            "range": "stddev: 7.246965013582401e-7",
            "extra": "mean: 3.3511449976199943 usec\nrounds: 41780"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 435752.2957642214,
            "unit": "iter/sec",
            "range": "stddev: 5.757586083173463e-7",
            "extra": "mean: 2.2948817704934914 usec\nrounds: 97666"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 449418.9154257366,
            "unit": "iter/sec",
            "range": "stddev: 5.482903688907929e-7",
            "extra": "mean: 2.225095485918067 usec\nrounds: 92422"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5819617.026295126,
            "unit": "iter/sec",
            "range": "stddev: 2.2007055255821924e-8",
            "extra": "mean: 171.83261295065682 nsec\nrounds: 193462"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 52629.937139457485,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020232195644447022",
            "extra": "mean: 19.00059271114509 usec\nrounds: 13747"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 88742.52386070734,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013202850647986294",
            "extra": "mean: 11.268554876460657 usec\nrounds: 38614"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20702.7881894456,
            "unit": "iter/sec",
            "range": "stddev: 0.000005408257895010322",
            "extra": "mean: 48.302672608600886 usec\nrounds: 7349"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43765.25823914715,
            "unit": "iter/sec",
            "range": "stddev: 0.000002736394966006844",
            "extra": "mean: 22.84917398489197 usec\nrounds: 16944"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9182.772533066312,
            "unit": "iter/sec",
            "range": "stddev: 0.000004945935025387477",
            "extra": "mean: 108.89957214981561 usec\nrounds: 4754"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4466.392076703203,
            "unit": "iter/sec",
            "range": "stddev: 0.00006599150311584468",
            "extra": "mean: 223.89436100247926 usec\nrounds: 1795"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19525.21652020451,
            "unit": "iter/sec",
            "range": "stddev: 0.000005236560496958765",
            "extra": "mean: 51.21582129269651 usec\nrounds: 9731"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1894258.5681440348,
            "unit": "iter/sec",
            "range": "stddev: 8.193633336638417e-8",
            "extra": "mean: 527.9110343313853 nsec\nrounds: 183790"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 244322.00202718773,
            "unit": "iter/sec",
            "range": "stddev: 7.919792571198925e-7",
            "extra": "mean: 4.0929592574667994 usec\nrounds: 30165"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1752441.5922098642,
            "unit": "iter/sec",
            "range": "stddev: 5.640844953347712e-8",
            "extra": "mean: 570.6324276059266 nsec\nrounds: 69171"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1280927.4725196338,
            "unit": "iter/sec",
            "range": "stddev: 1.1642029932570624e-7",
            "extra": "mean: 780.6843255792944 nsec\nrounds: 156446"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 285534.43603118,
            "unit": "iter/sec",
            "range": "stddev: 6.425512446051044e-7",
            "extra": "mean: 3.5022045463223956 usec\nrounds: 53494"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 148176.23770617234,
            "unit": "iter/sec",
            "range": "stddev: 9.809295161225622e-7",
            "extra": "mean: 6.748720412128163 usec\nrounds: 23971"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64302.6170520847,
            "unit": "iter/sec",
            "range": "stddev: 0.00040582778902836287",
            "extra": "mean: 15.551466578568746 usec\nrounds: 23458"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 7970209.8373584775,
            "unit": "iter/sec",
            "range": "stddev: 1.0913893488205951e-8",
            "extra": "mean: 125.46721107805598 nsec\nrounds: 77919"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "4cbb0b8538ecab84619aa23bdb3c8494121c84e4",
          "message": "Merge pull request #7 from nikolasil/refactor/service-layer\n\nRefactor/service layer",
          "timestamp": "2026-02-13T13:33:08-05:00",
          "tree_id": "2a3e9dbd387d8c855be01f4b1ac87a35836b4fc0",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/4cbb0b8538ecab84619aa23bdb3c8494121c84e4"
        },
        "date": 1771007679329,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 200808.2875622288,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019048679059906653",
            "extra": "mean: 4.979874148322232 usec\nrounds: 13063"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 207330.1396613699,
            "unit": "iter/sec",
            "range": "stddev: 7.505177733293075e-7",
            "extra": "mean: 4.823225420256261 usec\nrounds: 37836"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 200241.04425699532,
            "unit": "iter/sec",
            "range": "stddev: 8.12884800413658e-7",
            "extra": "mean: 4.993981147624112 usec\nrounds: 36388"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 310389.9271689967,
            "unit": "iter/sec",
            "range": "stddev: 7.405135768448365e-7",
            "extra": "mean: 3.221754034097679 usec\nrounds: 43876"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 440011.87176501437,
            "unit": "iter/sec",
            "range": "stddev: 5.640474272792331e-7",
            "extra": "mean: 2.2726659532814693 usec\nrounds: 100929"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 446610.9077901452,
            "unit": "iter/sec",
            "range": "stddev: 5.281128473963275e-7",
            "extra": "mean: 2.2390854825916677 usec\nrounds: 101740"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5631880.271195269,
            "unit": "iter/sec",
            "range": "stddev: 2.3056617217610387e-8",
            "extra": "mean: 177.5605928830627 nsec\nrounds: 199204"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 52373.75076291122,
            "unit": "iter/sec",
            "range": "stddev: 0.000002008855059472649",
            "extra": "mean: 19.093534173766987 usec\nrounds: 13168"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 90209.09779784486,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013583795135008357",
            "extra": "mean: 11.085356404305935 usec\nrounds: 37623"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20585.567556744838,
            "unit": "iter/sec",
            "range": "stddev: 0.000004875017544676315",
            "extra": "mean: 48.577723069498326 usec\nrounds: 6164"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43493.46189266131,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027291263616138",
            "extra": "mean: 22.991961469241673 usec\nrounds: 17233"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9178.825476446713,
            "unit": "iter/sec",
            "range": "stddev: 0.000005434594459993481",
            "extra": "mean: 108.94640088386535 usec\nrounds: 4752"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4508.173256441382,
            "unit": "iter/sec",
            "range": "stddev: 0.00006537266338557622",
            "extra": "mean: 221.81933637336962 usec\nrounds: 1864"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19672.74710999772,
            "unit": "iter/sec",
            "range": "stddev: 0.0000052376695319537485",
            "extra": "mean: 50.83174171907078 usec\nrounds: 9540"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1944753.7912538168,
            "unit": "iter/sec",
            "range": "stddev: 8.032113317932895e-8",
            "extra": "mean: 514.2039082259778 nsec\nrounds: 169751"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 244731.40820410478,
            "unit": "iter/sec",
            "range": "stddev: 8.287741823724674e-7",
            "extra": "mean: 4.086112229477325 usec\nrounds: 33182"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1762648.7385354755,
            "unit": "iter/sec",
            "range": "stddev: 5.44141491824896e-8",
            "extra": "mean: 567.3280093405649 nsec\nrounds: 67440"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1292812.3294619953,
            "unit": "iter/sec",
            "range": "stddev: 1.3232814608585377e-7",
            "extra": "mean: 773.5074745273631 nsec\nrounds: 151470"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 284487.41700296977,
            "unit": "iter/sec",
            "range": "stddev: 6.924620226701099e-7",
            "extra": "mean: 3.5150939557708485 usec\nrounds: 45266"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 146310.65029709705,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010286082094838608",
            "extra": "mean: 6.834772437750836 usec\nrounds: 24345"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 63452.155448542115,
            "unit": "iter/sec",
            "range": "stddev: 0.00043934527866291685",
            "extra": "mean: 15.75990591542586 usec\nrounds: 22044"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8234385.5723038735,
            "unit": "iter/sec",
            "range": "stddev: 1.0580355279622409e-8",
            "extra": "mean: 121.44196931510291 nsec\nrounds: 80561"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "409a6768cf8c4075c25d0c008a5c21783fb8c314",
          "message": "Merge pull request #13 from nikolasil/add-create-release-workflow\n\nfix: resolve benchmark CI issues - permissions and summary size",
          "timestamp": "2026-02-14T17:41:19-05:00",
          "tree_id": "ba50a905654fc7f1ac847d3328722d06ef34b04c",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/409a6768cf8c4075c25d0c008a5c21783fb8c314"
        },
        "date": 1771109020499,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 205362.0845073412,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019433236856921686",
            "extra": "mean: 4.869448040513303 usec\nrounds: 15387"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 199792.90036397145,
            "unit": "iter/sec",
            "range": "stddev: 8.628921893569579e-7",
            "extra": "mean: 5.005182857740472 usec\nrounds: 37953"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 199457.81935250942,
            "unit": "iter/sec",
            "range": "stddev: 7.588183880757218e-7",
            "extra": "mean: 5.013591361051942 usec\nrounds: 22225"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 307808.08899384993,
            "unit": "iter/sec",
            "range": "stddev: 7.092553869127156e-7",
            "extra": "mean: 3.248777520008515 usec\nrounds: 46993"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 429351.3573702524,
            "unit": "iter/sec",
            "range": "stddev: 7.206584354511035e-7",
            "extra": "mean: 2.3290947678026024 usec\nrounds: 95887"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 444335.31979406724,
            "unit": "iter/sec",
            "range": "stddev: 5.919508959134003e-7",
            "extra": "mean: 2.2505525792175662 usec\nrounds: 88961"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5896288.28967601,
            "unit": "iter/sec",
            "range": "stddev: 2.480576914085623e-8",
            "extra": "mean: 169.59822024828694 nsec\nrounds: 197668"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 51290.07430920149,
            "unit": "iter/sec",
            "range": "stddev: 0.000002427245356390301",
            "extra": "mean: 19.496949721139302 usec\nrounds: 12192"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 89801.00653812608,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014137028914283343",
            "extra": "mean: 11.135732644326634 usec\nrounds: 34254"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 21161.830840551873,
            "unit": "iter/sec",
            "range": "stddev: 0.0000053282094341712965",
            "extra": "mean: 47.25489054017603 usec\nrounds: 6998"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42486.351355288556,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027316670619846786",
            "extra": "mean: 23.536970535256927 usec\nrounds: 16664"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 8939.083080321707,
            "unit": "iter/sec",
            "range": "stddev: 0.000006221859231776179",
            "extra": "mean: 111.86829689516783 usec\nrounds: 4638"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4523.903568452108,
            "unit": "iter/sec",
            "range": "stddev: 0.0000633630977612194",
            "extra": "mean: 221.04803625205446 usec\nrounds: 1793"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 20062.91229435159,
            "unit": "iter/sec",
            "range": "stddev: 0.00000547371818698063",
            "extra": "mean: 49.8432124573228 usec\nrounds: 9376"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1911245.1254295434,
            "unit": "iter/sec",
            "range": "stddev: 9.774422904748071e-8",
            "extra": "mean: 523.219123855319 nsec\nrounds: 178891"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 242871.69515740924,
            "unit": "iter/sec",
            "range": "stddev: 8.708289845958605e-7",
            "extra": "mean: 4.117400339104494 usec\nrounds: 27719"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1780456.6514909521,
            "unit": "iter/sec",
            "range": "stddev: 5.986226651134169e-8",
            "extra": "mean: 561.6536629310203 nsec\nrounds: 67719"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1296348.9989585334,
            "unit": "iter/sec",
            "range": "stddev: 1.2804161625415156e-7",
            "extra": "mean: 771.3972092416909 nsec\nrounds: 158153"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 285653.4244624677,
            "unit": "iter/sec",
            "range": "stddev: 7.415584772994445e-7",
            "extra": "mean: 3.5007457091815506 usec\nrounds: 39561"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 148316.0368968774,
            "unit": "iter/sec",
            "range": "stddev: 9.76533882593632e-7",
            "extra": "mean: 6.7423592277839095 usec\nrounds: 23879"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64619.09341346847,
            "unit": "iter/sec",
            "range": "stddev: 0.0004206903400349637",
            "extra": "mean: 15.475302223778511 usec\nrounds: 23294"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8033020.602997869,
            "unit": "iter/sec",
            "range": "stddev: 1.1179051547207441e-8",
            "extra": "mean: 124.48617393404739 nsec\nrounds: 78846"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "3baac68beccd66a7867ba0300e88961d2188cbca",
          "message": "Merge pull request #14 from nikolasil/add-create-release-workflow\n\nfix: add -u flag to git-cliff for unreleased changelog",
          "timestamp": "2026-02-14T17:47:31-05:00",
          "tree_id": "e415ca443adcd028720ece55d6a3d6b541a8a52d",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/3baac68beccd66a7867ba0300e88961d2188cbca"
        },
        "date": 1771109401715,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 203408.0796334615,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017262201901549167",
            "extra": "mean: 4.916225558994442 usec\nrounds: 16683"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 203542.28943985893,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017462260552939167",
            "extra": "mean: 4.912983944279905 usec\nrounds: 37370"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 201149.4249694333,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018760302717217328",
            "extra": "mean: 4.971428579286071 usec\nrounds: 36348"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 305879.75728789216,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010352629246409738",
            "extra": "mean: 3.269258511470591 usec\nrounds: 44323"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 440804.68253454496,
            "unit": "iter/sec",
            "range": "stddev: 5.620824523797461e-7",
            "extra": "mean: 2.2685784421576147 usec\nrounds: 97097"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 445139.495621558,
            "unit": "iter/sec",
            "range": "stddev: 5.207945019973799e-7",
            "extra": "mean: 2.2464867975906704 usec\nrounds: 93809"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5803608.470246814,
            "unit": "iter/sec",
            "range": "stddev: 2.32248312092322e-8",
            "extra": "mean: 172.306592549558 nsec\nrounds: 191571"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 50828.44191859647,
            "unit": "iter/sec",
            "range": "stddev: 0.000002121789362182132",
            "extra": "mean: 19.67402427171651 usec\nrounds: 13184"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 88676.84207460815,
            "unit": "iter/sec",
            "range": "stddev: 0.000001340983925426292",
            "extra": "mean: 11.276901348817216 usec\nrounds: 38702"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20041.09799400459,
            "unit": "iter/sec",
            "range": "stddev: 0.00000863691854116887",
            "extra": "mean: 49.89746571266483 usec\nrounds: 7408"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42475.491600550384,
            "unit": "iter/sec",
            "range": "stddev: 0.000002837277146623971",
            "extra": "mean: 23.542988257893228 usec\nrounds: 16692"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9117.118451045286,
            "unit": "iter/sec",
            "range": "stddev: 0.0000073758847843022474",
            "extra": "mean: 109.68377841853629 usec\nrounds: 4161"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4429.050977097437,
            "unit": "iter/sec",
            "range": "stddev: 0.00006438162632966876",
            "extra": "mean: 225.782002774632 usec\nrounds: 1802"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19665.483551043108,
            "unit": "iter/sec",
            "range": "stddev: 0.000006440033227545329",
            "extra": "mean: 50.85051671393849 usec\nrounds: 9483"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1937023.6136432996,
            "unit": "iter/sec",
            "range": "stddev: 1.0446883217138329e-7",
            "extra": "mean: 516.2559676384736 nsec\nrounds: 177936"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 243321.59898731302,
            "unit": "iter/sec",
            "range": "stddev: 8.314165081215542e-7",
            "extra": "mean: 4.1097872287619674 usec\nrounds: 36034"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1782407.7208255033,
            "unit": "iter/sec",
            "range": "stddev: 6.209885917642776e-8",
            "extra": "mean: 561.0388623860118 nsec\nrounds: 69171"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1296322.4115729423,
            "unit": "iter/sec",
            "range": "stddev: 1.2313956087473613e-7",
            "extra": "mean: 771.4130304872278 nsec\nrounds: 159439"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 285465.9012368432,
            "unit": "iter/sec",
            "range": "stddev: 6.878285241283235e-7",
            "extra": "mean: 3.503045357316871 usec\nrounds: 52340"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 146523.92159431972,
            "unit": "iter/sec",
            "range": "stddev: 9.444376244882574e-7",
            "extra": "mean: 6.824824159216108 usec\nrounds: 28486"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 61556.668938089104,
            "unit": "iter/sec",
            "range": "stddev: 0.0004274572460545556",
            "extra": "mean: 16.245193530627112 usec\nrounds: 18178"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8107964.77657223,
            "unit": "iter/sec",
            "range": "stddev: 1.0624365973211877e-8",
            "extra": "mean: 123.33551360389123 nsec\nrounds: 80490"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "e9a34cfc57e0bd3a5dd88ea00552ff50d25b4b4e",
          "message": "Merge pull request #15 from nikolasil/add-create-release-workflow\n\nfix: remove conflicting OUTPUT env from git-cliff action",
          "timestamp": "2026-02-14T17:50:49-05:00",
          "tree_id": "ed0ac0ba34f6fca055316a5ffeec09f966f4c359",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/e9a34cfc57e0bd3a5dd88ea00552ff50d25b4b4e"
        },
        "date": 1771109598432,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 208528.27298638807,
            "unit": "iter/sec",
            "range": "stddev: 0.000001787346377211716",
            "extra": "mean: 4.79551278912321 usec\nrounds: 15521"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 209099.04187807778,
            "unit": "iter/sec",
            "range": "stddev: 7.706914089602418e-7",
            "extra": "mean: 4.782422678833141 usec\nrounds: 38450"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 203450.45938345033,
            "unit": "iter/sec",
            "range": "stddev: 6.964351115507064e-7",
            "extra": "mean: 4.915201484579911 usec\nrounds: 36509"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 306044.0704860228,
            "unit": "iter/sec",
            "range": "stddev: 7.504951945598198e-7",
            "extra": "mean: 3.2675032664802783 usec\nrounds: 43778"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 433952.18143407936,
            "unit": "iter/sec",
            "range": "stddev: 4.928693710856227e-7",
            "extra": "mean: 2.3044013667480723 usec\nrounds: 41852"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 439237.20982783375,
            "unit": "iter/sec",
            "range": "stddev: 5.361086217413561e-7",
            "extra": "mean: 2.27667414696484 usec\nrounds: 97857"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5670318.081316582,
            "unit": "iter/sec",
            "range": "stddev: 2.1879280076523074e-8",
            "extra": "mean: 176.3569495853478 nsec\nrounds: 197239"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 51458.299214892904,
            "unit": "iter/sec",
            "range": "stddev: 0.000002169957554326658",
            "extra": "mean: 19.433211265377054 usec\nrounds: 12605"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 86270.1158141504,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013304208891563058",
            "extra": "mean: 11.591499449870632 usec\nrounds: 39081"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 21042.054647012363,
            "unit": "iter/sec",
            "range": "stddev: 0.000005203421215640608",
            "extra": "mean: 47.52387619818221 usec\nrounds: 7407"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42990.3051653305,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028930897849841025",
            "extra": "mean: 23.261058421293768 usec\nrounds: 16672"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9116.077588478012,
            "unit": "iter/sec",
            "range": "stddev: 0.000005553405707971126",
            "extra": "mean: 109.69630197793833 usec\nrounds: 4348"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4476.774785869503,
            "unit": "iter/sec",
            "range": "stddev: 0.00005621957259855532",
            "extra": "mean: 223.3750965441463 usec\nrounds: 1823"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19879.507281720256,
            "unit": "iter/sec",
            "range": "stddev: 0.000005723391590114814",
            "extra": "mean: 50.303057607445176 usec\nrounds: 9287"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1872453.411784999,
            "unit": "iter/sec",
            "range": "stddev: 7.73961645457176e-8",
            "extra": "mean: 534.0586813568102 nsec\nrounds: 181160"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 245964.92103837573,
            "unit": "iter/sec",
            "range": "stddev: 6.689949080360651e-7",
            "extra": "mean: 4.065620397324783 usec\nrounds: 33975"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1767339.755804413,
            "unit": "iter/sec",
            "range": "stddev: 5.344316866884398e-8",
            "extra": "mean: 565.8221610845975 nsec\nrounds: 69604"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1283862.8895685463,
            "unit": "iter/sec",
            "range": "stddev: 1.1480335842344425e-7",
            "extra": "mean: 778.8993732314013 nsec\nrounds: 157208"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 287795.3654385482,
            "unit": "iter/sec",
            "range": "stddev: 6.554021373580427e-7",
            "extra": "mean: 3.4746911176841935 usec\nrounds: 53263"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 146941.18472539005,
            "unit": "iter/sec",
            "range": "stddev: 9.430000792733426e-7",
            "extra": "mean: 6.805443973170916 usec\nrounds: 17447"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 65021.19507943279,
            "unit": "iter/sec",
            "range": "stddev: 0.0003890968670892543",
            "extra": "mean: 15.379600433033497 usec\nrounds: 23553"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8060605.814442196,
            "unit": "iter/sec",
            "range": "stddev: 1.0656761987866767e-8",
            "extra": "mean: 124.06015416473339 nsec\nrounds: 80109"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "83906c0717d09a5a60e4a2eb1e0ff8983d9d7fa1",
          "message": "Merge pull request #16 from nikolasil/add-create-release-workflow\n\nAdd create release workflow",
          "timestamp": "2026-02-14T18:14:52-05:00",
          "tree_id": "26b68aec8c7051f7d86d83354ac33915bea68313",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/83906c0717d09a5a60e4a2eb1e0ff8983d9d7fa1"
        },
        "date": 1771111057795,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 207330.571012988,
            "unit": "iter/sec",
            "range": "stddev: 0.000001629079327257537",
            "extra": "mean: 4.823215385527281 usec\nrounds: 16756"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 206169.5988738288,
            "unit": "iter/sec",
            "range": "stddev: 7.799387899403793e-7",
            "extra": "mean: 4.850375639581943 usec\nrounds: 37134"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 204037.61647688737,
            "unit": "iter/sec",
            "range": "stddev: 7.213987721334858e-7",
            "extra": "mean: 4.901057056375074 usec\nrounds: 36350"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 307385.15280343307,
            "unit": "iter/sec",
            "range": "stddev: 6.477380283718603e-7",
            "extra": "mean: 3.253247565406911 usec\nrounds: 41383"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 436283.6942086843,
            "unit": "iter/sec",
            "range": "stddev: 5.778368017591622e-7",
            "extra": "mean: 2.2920865786968365 usec\nrounds: 99424"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 449161.53889163287,
            "unit": "iter/sec",
            "range": "stddev: 5.039932745523242e-7",
            "extra": "mean: 2.2263705001715772 usec\nrounds: 100726"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5667810.905806347,
            "unit": "iter/sec",
            "range": "stddev: 2.1907228900039464e-8",
            "extra": "mean: 176.4349616842714 nsec\nrounds: 196503"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 51170.85378507489,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018188170889435011",
            "extra": "mean: 19.542374731524845 usec\nrounds: 13503"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 88430.11618104897,
            "unit": "iter/sec",
            "range": "stddev: 0.000001337682484796155",
            "extra": "mean: 11.30836465206754 usec\nrounds: 38039"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20650.95485971584,
            "unit": "iter/sec",
            "range": "stddev: 0.0000050018418530077734",
            "extra": "mean: 48.42391099070759 usec\nrounds: 6460"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43048.505882359364,
            "unit": "iter/sec",
            "range": "stddev: 0.000002681096449263409",
            "extra": "mean: 23.229609936585167 usec\nrounds: 17028"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9122.272062402493,
            "unit": "iter/sec",
            "range": "stddev: 0.000005119047160298192",
            "extra": "mean: 109.62181276323767 usec\nrounds: 4748"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4572.556431293821,
            "unit": "iter/sec",
            "range": "stddev: 0.00008171799478438444",
            "extra": "mean: 218.69604345529015 usec\nrounds: 1887"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19925.129966645083,
            "unit": "iter/sec",
            "range": "stddev: 0.0000051418290933210255",
            "extra": "mean: 50.187878406515416 usec\nrounds: 9614"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1902152.9854296376,
            "unit": "iter/sec",
            "range": "stddev: 7.128968434922987e-8",
            "extra": "mean: 525.7200696578728 nsec\nrounds: 165810"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 244610.84693145027,
            "unit": "iter/sec",
            "range": "stddev: 6.83207942322872e-7",
            "extra": "mean: 4.088126150351132 usec\nrounds: 35751"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1760525.3654830311,
            "unit": "iter/sec",
            "range": "stddev: 5.3048579697090125e-8",
            "extra": "mean: 568.012264751356 nsec\nrounds: 69076"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1288313.6030201537,
            "unit": "iter/sec",
            "range": "stddev: 1.2493132266147712e-7",
            "extra": "mean: 776.2085238063752 nsec\nrounds: 159694"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 286803.9505669032,
            "unit": "iter/sec",
            "range": "stddev: 6.33232583939544e-7",
            "extra": "mean: 3.4867023206039427 usec\nrounds: 52701"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 149609.11112705618,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010638300486103408",
            "extra": "mean: 6.684084896077925 usec\nrounds: 30449"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 65363.42438619958,
            "unit": "iter/sec",
            "range": "stddev: 0.0003867421875957556",
            "extra": "mean: 15.299076041235283 usec\nrounds: 24513"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8030671.844448482,
            "unit": "iter/sec",
            "range": "stddev: 1.011019453184154e-8",
            "extra": "mean: 124.52258283872972 nsec\nrounds: 79854"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "38adc60ecea124b4e316f406a480d4d613bae342",
          "message": "Merge pull request #17 from nikolasil/add-create-release-workflow\n\nfix: add checkout step to create-tag job",
          "timestamp": "2026-02-15T13:54:25-05:00",
          "tree_id": "c49e81c1ba4aaf5c32005362933f3fe8edf8548f",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/38adc60ecea124b4e316f406a480d4d613bae342"
        },
        "date": 1771181814390,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 207550.8123383504,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016944569063453106",
            "extra": "mean: 4.818097258852424 usec\nrounds: 16708"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 208481.01814945097,
            "unit": "iter/sec",
            "range": "stddev: 7.922537567217035e-7",
            "extra": "mean: 4.796599752228491 usec\nrounds: 37132"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 189240.04091698487,
            "unit": "iter/sec",
            "range": "stddev: 0.000001818293481739528",
            "extra": "mean: 5.284293932480581 usec\nrounds: 37808"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 304655.21434910235,
            "unit": "iter/sec",
            "range": "stddev: 6.588057581796682e-7",
            "extra": "mean: 3.28239909543812 usec\nrounds: 43115"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 431859.3753406785,
            "unit": "iter/sec",
            "range": "stddev: 6.311959006354689e-7",
            "extra": "mean: 2.315568578802152 usec\nrounds: 96349"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 451433.74252458813,
            "unit": "iter/sec",
            "range": "stddev: 5.353556046227369e-7",
            "extra": "mean: 2.215164498798034 usec\nrounds: 102481"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5788890.448376119,
            "unit": "iter/sec",
            "range": "stddev: 2.2740088609152064e-8",
            "extra": "mean: 172.74467515284806 nsec\nrounds: 195351"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 51903.349411595045,
            "unit": "iter/sec",
            "range": "stddev: 0.000001992531865789146",
            "extra": "mean: 19.26657935059203 usec\nrounds: 13705"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 89357.3911252374,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014164800450852272",
            "extra": "mean: 11.191016069375463 usec\nrounds: 37836"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 21003.790768331073,
            "unit": "iter/sec",
            "range": "stddev: 0.000005679622811415642",
            "extra": "mean: 47.610453323871994 usec\nrounds: 7145"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43818.756792065695,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029186520156320155",
            "extra": "mean: 22.82127730700637 usec\nrounds: 17230"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9148.116009330863,
            "unit": "iter/sec",
            "range": "stddev: 0.00000580182830279908",
            "extra": "mean: 109.31212492058731 usec\nrounds: 4715"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4433.219568403475,
            "unit": "iter/sec",
            "range": "stddev: 0.00006931590206135371",
            "extra": "mean: 225.56969817764465 usec\nrounds: 1756"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 20048.625359670696,
            "unit": "iter/sec",
            "range": "stddev: 0.000005683894878544157",
            "extra": "mean: 49.87873143719741 usec\nrounds: 9212"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1882809.9104479977,
            "unit": "iter/sec",
            "range": "stddev: 1.1447893324697614e-7",
            "extra": "mean: 531.1210624348472 nsec\nrounds: 166918"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 244400.78121876897,
            "unit": "iter/sec",
            "range": "stddev: 7.872024027006686e-7",
            "extra": "mean: 4.091639948993764 usec\nrounds: 35295"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1768772.5006509735,
            "unit": "iter/sec",
            "range": "stddev: 6.104739323809657e-8",
            "extra": "mean: 565.3638326194358 nsec\nrounds: 69459"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1292761.1140022224,
            "unit": "iter/sec",
            "range": "stddev: 1.3171876786816895e-7",
            "extra": "mean: 773.5381186580872 nsec\nrounds: 180148"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 285524.5803025271,
            "unit": "iter/sec",
            "range": "stddev: 6.869904240198872e-7",
            "extra": "mean: 3.5023254353108637 usec\nrounds: 53009"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 148945.4276508274,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010422373239017266",
            "extra": "mean: 6.713868399802772 usec\nrounds: 28389"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64338.20865254859,
            "unit": "iter/sec",
            "range": "stddev: 0.0004295810759936361",
            "extra": "mean: 15.542863578940937 usec\nrounds: 24549"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8129997.939265755,
            "unit": "iter/sec",
            "range": "stddev: 1.1010987655358637e-8",
            "extra": "mean: 123.00126118989931 nsec\nrounds: 77078"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "bdec3542dc3be0eca7c96d1dd5382dedb09fd247",
          "message": "Merge pull request #18 from nikolasil/add-create-release-workflow\n\nfix: use release files from prepare for building, only commit if chan…",
          "timestamp": "2026-02-15T14:17:32-05:00",
          "tree_id": "02399e607158f4023c19b085447af1972409040a",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/bdec3542dc3be0eca7c96d1dd5382dedb09fd247"
        },
        "date": 1771183203230,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 206401.73961688284,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016267513041212174",
            "extra": "mean: 4.844920405497416 usec\nrounds: 17363"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 201607.20949982488,
            "unit": "iter/sec",
            "range": "stddev: 0.000001193045416302562",
            "extra": "mean: 4.960140078725054 usec\nrounds: 38614"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 203621.60832020146,
            "unit": "iter/sec",
            "range": "stddev: 7.28371838248255e-7",
            "extra": "mean: 4.9110701376421115 usec\nrounds: 38567"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 309758.00159627583,
            "unit": "iter/sec",
            "range": "stddev: 6.241820088898427e-7",
            "extra": "mean: 3.2283266125384986 usec\nrounds: 44340"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 431875.5355149708,
            "unit": "iter/sec",
            "range": "stddev: 5.186976049082276e-7",
            "extra": "mean: 2.3154819334871437 usec\nrounds: 106191"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 439940.853038138,
            "unit": "iter/sec",
            "range": "stddev: 6.479633376784003e-7",
            "extra": "mean: 2.273032824967749 usec\nrounds: 108850"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5733330.514900015,
            "unit": "iter/sec",
            "range": "stddev: 2.3880585873637866e-8",
            "extra": "mean: 174.41869039316308 nsec\nrounds: 198020"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 52226.08826654825,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017891907380350666",
            "extra": "mean: 19.14751866722743 usec\nrounds: 10955"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 87522.65902649522,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015283689100013874",
            "extra": "mean: 11.42561264846028 usec\nrounds: 40005"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20846.487555179134,
            "unit": "iter/sec",
            "range": "stddev: 0.000005858849089287324",
            "extra": "mean: 47.96971179691893 usec\nrounds: 7519"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42648.98918852831,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025977931811164353",
            "extra": "mean: 23.447214553656508 usec\nrounds: 17329"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9121.822466620875,
            "unit": "iter/sec",
            "range": "stddev: 0.000004705256969197409",
            "extra": "mean: 109.62721579588514 usec\nrounds: 4824"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4071.555111793739,
            "unit": "iter/sec",
            "range": "stddev: 0.00007782811018664732",
            "extra": "mean: 245.6064016187285 usec\nrounds: 1977"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19999.965064861855,
            "unit": "iter/sec",
            "range": "stddev: 0.000005027187564400521",
            "extra": "mean: 50.000087337997925 usec\nrounds: 9572"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1892373.9262112686,
            "unit": "iter/sec",
            "range": "stddev: 7.730462074865371e-8",
            "extra": "mean: 528.4367883899746 nsec\nrounds: 181819"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 243444.13531141434,
            "unit": "iter/sec",
            "range": "stddev: 7.346428596176294e-7",
            "extra": "mean: 4.107718588992902 usec\nrounds: 36683"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1730322.6922954987,
            "unit": "iter/sec",
            "range": "stddev: 6.162606189783092e-8",
            "extra": "mean: 577.9268829176427 nsec\nrounds: 67714"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1277736.689925303,
            "unit": "iter/sec",
            "range": "stddev: 1.2551219529877484e-7",
            "extra": "mean: 782.6338618002045 nsec\nrounds: 181786"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 286497.57940331835,
            "unit": "iter/sec",
            "range": "stddev: 6.364290758703275e-7",
            "extra": "mean: 3.4904308863016436 usec\nrounds: 53752"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 147141.7154140971,
            "unit": "iter/sec",
            "range": "stddev: 9.688014409511808e-7",
            "extra": "mean: 6.796169238517615 usec\nrounds: 29875"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 65753.26865256767,
            "unit": "iter/sec",
            "range": "stddev: 0.00037186540835013634",
            "extra": "mean: 15.208369416338513 usec\nrounds: 23954"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8141804.73269818,
            "unit": "iter/sec",
            "range": "stddev: 1.0212498718917436e-8",
            "extra": "mean: 122.82289158626159 nsec\nrounds: 80174"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "a10a2f8736862a1295c5e305c1715a075c480fc5",
          "message": "Merge pull request #19 from nikolasil/add-create-release-workflow\n\nfix: checkout main before downloading release files in all jobs",
          "timestamp": "2026-02-15T14:30:24-05:00",
          "tree_id": "a9bdf56b1fd3ffd4006b93adec7ad9750a8932b8",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/a10a2f8736862a1295c5e305c1715a075c480fc5"
        },
        "date": 1771183972751,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 203780.43992652558,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017358279523272213",
            "extra": "mean: 4.9072423259099685 usec\nrounds: 18178"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 201827.29741657324,
            "unit": "iter/sec",
            "range": "stddev: 8.708937219259588e-7",
            "extra": "mean: 4.954731162732618 usec\nrounds: 35382"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 195236.84705510116,
            "unit": "iter/sec",
            "range": "stddev: 0.000001212794638620848",
            "extra": "mean: 5.121983965033879 usec\nrounds: 37356"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 303740.5023092354,
            "unit": "iter/sec",
            "range": "stddev: 6.535016530991878e-7",
            "extra": "mean: 3.2922840134830267 usec\nrounds: 44600"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 427304.2136162723,
            "unit": "iter/sec",
            "range": "stddev: 5.243900802742915e-7",
            "extra": "mean: 2.3402530752903363 usec\nrounds: 103649"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 433185.2808863331,
            "unit": "iter/sec",
            "range": "stddev: 5.896855783687055e-7",
            "extra": "mean: 2.308481022148114 usec\nrounds: 106519"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5359232.095813978,
            "unit": "iter/sec",
            "range": "stddev: 2.496013972996636e-8",
            "extra": "mean: 186.59389668561292 nsec\nrounds: 194175"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 48945.6148951344,
            "unit": "iter/sec",
            "range": "stddev: 0.000002053037004642423",
            "extra": "mean: 20.430839456047128 usec\nrounds: 13311"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 85289.6218982818,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017762812949418184",
            "extra": "mean: 11.724755928600798 usec\nrounds: 38837"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20621.7967908335,
            "unit": "iter/sec",
            "range": "stddev: 0.000004752868679102774",
            "extra": "mean: 48.49237969624962 usec\nrounds: 7506"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42536.68727867516,
            "unit": "iter/sec",
            "range": "stddev: 0.000002941988282972408",
            "extra": "mean: 23.50911798675324 usec\nrounds: 17663"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9131.893806557955,
            "unit": "iter/sec",
            "range": "stddev: 0.0000059852522886036734",
            "extra": "mean: 109.50631064958975 usec\nrounds: 4188"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4429.5987236859955,
            "unit": "iter/sec",
            "range": "stddev: 0.00008168020558173784",
            "extra": "mean: 225.7540834687327 usec\nrounds: 1845"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 18369.71663178949,
            "unit": "iter/sec",
            "range": "stddev: 0.000013223463517556772",
            "extra": "mean: 54.43742111239005 usec\nrounds: 9691"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1847302.6250796563,
            "unit": "iter/sec",
            "range": "stddev: 8.817999168389839e-8",
            "extra": "mean: 541.3298213425373 nsec\nrounds: 183453"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 235450.8279165147,
            "unit": "iter/sec",
            "range": "stddev: 7.298797808779869e-7",
            "extra": "mean: 4.24717130472175 usec\nrounds: 24903"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1625507.7899452369,
            "unit": "iter/sec",
            "range": "stddev: 1.1506391945854966e-7",
            "extra": "mean: 615.1923763057704 nsec\nrounds: 140588"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1250577.4149199084,
            "unit": "iter/sec",
            "range": "stddev: 1.4236808687577618e-7",
            "extra": "mean: 799.630625077324 nsec\nrounds: 172682"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 277484.95913138933,
            "unit": "iter/sec",
            "range": "stddev: 6.877852582007982e-7",
            "extra": "mean: 3.6037989342928647 usec\nrounds: 55176"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 144504.36245218178,
            "unit": "iter/sec",
            "range": "stddev: 0.000001485741469769767",
            "extra": "mean: 6.920206304020143 usec\nrounds: 30552"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 65402.57541136568,
            "unit": "iter/sec",
            "range": "stddev: 0.00034271340206417435",
            "extra": "mean: 15.289917770213982 usec\nrounds: 27788"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 7891687.447632906,
            "unit": "iter/sec",
            "range": "stddev: 1.0675551192901561e-8",
            "extra": "mean: 126.71561141204339 nsec\nrounds: 78654"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "0d0bd73155a265381c7a28e6ebf5a8f0cad30b2f",
          "message": "Merge pull request #20 from nikolasil/add-create-release-workflow\n\nfix: correct workflow version output ref and PyPI publishing",
          "timestamp": "2026-02-15T14:47:57-05:00",
          "tree_id": "1dbd56af0284898405fdaf90caec915ff3f67fa0",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/0d0bd73155a265381c7a28e6ebf5a8f0cad30b2f"
        },
        "date": 1771185030958,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 206260.73528538374,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015811798263638507",
            "extra": "mean: 4.848232498620706 usec\nrounds: 17570"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 207919.97556165775,
            "unit": "iter/sec",
            "range": "stddev: 7.833298379397218e-7",
            "extra": "mean: 4.80954269688943 usec\nrounds: 36361"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 198846.19270206647,
            "unit": "iter/sec",
            "range": "stddev: 7.856591294580494e-7",
            "extra": "mean: 5.02901255694803 usec\nrounds: 36872"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 307196.7716714977,
            "unit": "iter/sec",
            "range": "stddev: 7.922823849289778e-7",
            "extra": "mean: 3.255242542292582 usec\nrounds: 44920"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 433314.99355698534,
            "unit": "iter/sec",
            "range": "stddev: 5.950331963851703e-7",
            "extra": "mean: 2.3077899792740264 usec\nrounds: 97857"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 446054.7860347139,
            "unit": "iter/sec",
            "range": "stddev: 5.566908896834396e-7",
            "extra": "mean: 2.2418770772300953 usec\nrounds: 102902"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5812432.22142708,
            "unit": "iter/sec",
            "range": "stddev: 2.182986915273529e-8",
            "extra": "mean: 172.0450169403157 nsec\nrounds: 199243"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 52164.13014446599,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018412868542073848",
            "extra": "mean: 19.1702611973122 usec\nrounds: 13664"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 89863.60950167189,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013143615080239007",
            "extra": "mean: 11.127975000619081 usec\nrounds: 37201"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20865.950499701074,
            "unit": "iter/sec",
            "range": "stddev: 0.0000051321629836145654",
            "extra": "mean: 47.924967521337024 usec\nrounds: 7605"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43097.04416543069,
            "unit": "iter/sec",
            "range": "stddev: 0.000002782250946407515",
            "extra": "mean: 23.20344746060629 usec\nrounds: 17130"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9123.647130108597,
            "unit": "iter/sec",
            "range": "stddev: 0.000005243246302499666",
            "extra": "mean: 109.60529114502232 usec\nrounds: 4314"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4521.094501835999,
            "unit": "iter/sec",
            "range": "stddev: 0.0000637418435650803",
            "extra": "mean: 221.18537880460227 usec\nrounds: 1840"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19851.035099887107,
            "unit": "iter/sec",
            "range": "stddev: 0.000005473454251408595",
            "extra": "mean: 50.37520688307519 usec\nrounds: 7613"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1754594.2144974296,
            "unit": "iter/sec",
            "range": "stddev: 1.2932691676194586e-7",
            "extra": "mean: 569.9323477403079 nsec\nrounds: 178254"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 251122.20874374558,
            "unit": "iter/sec",
            "range": "stddev: 7.453245022474034e-7",
            "extra": "mean: 3.982124898480951 usec\nrounds: 36942"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1759438.1922029923,
            "unit": "iter/sec",
            "range": "stddev: 5.420645779680404e-8",
            "extra": "mean: 568.3632448310866 nsec\nrounds: 67079"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1268838.890380498,
            "unit": "iter/sec",
            "range": "stddev: 1.3230646353017796e-7",
            "extra": "mean: 788.12212297511 nsec\nrounds: 160206"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 287181.5858164115,
            "unit": "iter/sec",
            "range": "stddev: 6.624664425288772e-7",
            "extra": "mean: 3.4821174106868984 usec\nrounds: 52508"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 147415.115899604,
            "unit": "iter/sec",
            "range": "stddev: 9.500602769064472e-7",
            "extra": "mean: 6.783564859665022 usec\nrounds: 25162"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 66537.226135424,
            "unit": "iter/sec",
            "range": "stddev: 0.00036248108821933304",
            "extra": "mean: 15.029180777159064 usec\nrounds: 26198"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 7997870.596753158,
            "unit": "iter/sec",
            "range": "stddev: 1.0596014856958723e-8",
            "extra": "mean: 125.03328078423105 nsec\nrounds: 80496"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "16b62eadb571582d44d6c3cbfa28c56243b702cb",
          "message": "Merge pull request #21 from nikolasil/add-create-release-workflow\n\nfix: add back PyPI password as fallback",
          "timestamp": "2026-02-15T14:58:48-05:00",
          "tree_id": "5048988938f1e257341aa95263221483fa3fd5d6",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/16b62eadb571582d44d6c3cbfa28c56243b702cb"
        },
        "date": 1771185689558,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 205592.00480394004,
            "unit": "iter/sec",
            "range": "stddev: 0.000001616824718698237",
            "extra": "mean: 4.864002376715165 usec\nrounds: 16830"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 207195.67764253725,
            "unit": "iter/sec",
            "range": "stddev: 7.265498964893752e-7",
            "extra": "mean: 4.826355507884881 usec\nrounds: 38272"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 202793.45477684384,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011088581700671555",
            "extra": "mean: 4.931125617936787 usec\nrounds: 36818"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 306510.29854331637,
            "unit": "iter/sec",
            "range": "stddev: 6.202239476253614e-7",
            "extra": "mean: 3.2625331179816097 usec\nrounds: 44266"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 433612.8996926275,
            "unit": "iter/sec",
            "range": "stddev: 5.534516205214282e-7",
            "extra": "mean: 2.3062044526555 usec\nrounds: 101647"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 446696.82422980183,
            "unit": "iter/sec",
            "range": "stddev: 5.512275904089987e-7",
            "extra": "mean: 2.238654823042917 usec\nrounds: 102052"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5546297.652732137,
            "unit": "iter/sec",
            "range": "stddev: 3.3791232709504e-8",
            "extra": "mean: 180.30045673935868 nsec\nrounds: 195313"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 51608.09168828878,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018959222163913456",
            "extra": "mean: 19.37680637447259 usec\nrounds: 13397"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 87747.8652645369,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013989286872383947",
            "extra": "mean: 11.396288638877552 usec\nrounds: 39468"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20666.604542333374,
            "unit": "iter/sec",
            "range": "stddev: 0.000005015261526541274",
            "extra": "mean: 48.38724222702403 usec\nrounds: 7526"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43216.0351313008,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025913986293668947",
            "extra": "mean: 23.13955912340772 usec\nrounds: 16973"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9201.722809338693,
            "unit": "iter/sec",
            "range": "stddev: 0.000005315209581735281",
            "extra": "mean: 108.67530143215298 usec\nrounds: 4817"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4519.6413973991885,
            "unit": "iter/sec",
            "range": "stddev: 0.0000622331401044548",
            "extra": "mean: 221.25649184810246 usec\nrounds: 1840"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19850.222828375034,
            "unit": "iter/sec",
            "range": "stddev: 0.000005334301673163735",
            "extra": "mean: 50.377268237540555 usec\nrounds: 9760"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1898041.4872157203,
            "unit": "iter/sec",
            "range": "stddev: 7.614379714860615e-8",
            "extra": "mean: 526.8588735997138 nsec\nrounds: 165536"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 248509.68816227582,
            "unit": "iter/sec",
            "range": "stddev: 7.182062140028615e-7",
            "extra": "mean: 4.023987987731907 usec\nrounds: 36629"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1769718.586421795,
            "unit": "iter/sec",
            "range": "stddev: 6.537387092907089e-8",
            "extra": "mean: 565.0615909628305 nsec\nrounds: 68933"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1269912.5271577218,
            "unit": "iter/sec",
            "range": "stddev: 1.3045889181927578e-7",
            "extra": "mean: 787.4558118094775 nsec\nrounds: 177905"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 286430.15971891285,
            "unit": "iter/sec",
            "range": "stddev: 9.255477003874865e-7",
            "extra": "mean: 3.4912524609187323 usec\nrounds: 53434"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 147229.30460444352,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010706286924308984",
            "extra": "mean: 6.792126083096497 usec\nrounds: 29084"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64938.78584869833,
            "unit": "iter/sec",
            "range": "stddev: 0.0003828367021969625",
            "extra": "mean: 15.399117598686125 usec\nrounds: 24286"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8075043.457752602,
            "unit": "iter/sec",
            "range": "stddev: 1.0809139278669759e-8",
            "extra": "mean: 123.83834281912411 nsec\nrounds: 78537"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "2f124043ea967ef582497af9e6a4c747fcbb7e2e",
          "message": "Merge pull request #22 from nikolasil/add-create-release-workflow\n\nfix: improve tag creation and explicitly set tag_name",
          "timestamp": "2026-02-15T15:16:52-05:00",
          "tree_id": "fa5e88fc922e40d2dc1931fb04daf156025f3ba4",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/2f124043ea967ef582497af9e6a4c747fcbb7e2e"
        },
        "date": 1771186762783,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 205095.38528054924,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017310110075896936",
            "extra": "mean: 4.875780109006859 usec\nrounds: 13393"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 202730.09481515785,
            "unit": "iter/sec",
            "range": "stddev: 7.240631642524611e-7",
            "extra": "mean: 4.932666760264502 usec\nrounds: 39173"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 199601.7415541258,
            "unit": "iter/sec",
            "range": "stddev: 8.623412099843156e-7",
            "extra": "mean: 5.009976326929146 usec\nrounds: 38567"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 305861.6358672312,
            "unit": "iter/sec",
            "range": "stddev: 6.65212979870765e-7",
            "extra": "mean: 3.2694522056178412 usec\nrounds: 43321"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 437243.4662764019,
            "unit": "iter/sec",
            "range": "stddev: 5.225280623570298e-7",
            "extra": "mean: 2.287055329873937 usec\nrounds: 98717"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 444649.17120522587,
            "unit": "iter/sec",
            "range": "stddev: 5.337258327554347e-7",
            "extra": "mean: 2.2489640479695265 usec\nrounds: 98242"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5800845.4149404755,
            "unit": "iter/sec",
            "range": "stddev: 2.1341202419895534e-8",
            "extra": "mean: 172.38866552537007 nsec\nrounds: 195695"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 52616.88139067835,
            "unit": "iter/sec",
            "range": "stddev: 0.000002007640581366102",
            "extra": "mean: 19.00530730004764 usec\nrounds: 13726"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 88432.91546051767,
            "unit": "iter/sec",
            "range": "stddev: 0.000001285274354500522",
            "extra": "mean: 11.30800669402861 usec\nrounds: 38243"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20406.02554338992,
            "unit": "iter/sec",
            "range": "stddev: 0.000005346833925990127",
            "extra": "mean: 49.005133208016 usec\nrounds: 7447"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42593.34590560187,
            "unit": "iter/sec",
            "range": "stddev: 0.000002661825132273206",
            "extra": "mean: 23.477845629133355 usec\nrounds: 17296"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9153.400585310492,
            "unit": "iter/sec",
            "range": "stddev: 0.000005205438642114593",
            "extra": "mean: 109.24901523536666 usec\nrounds: 4332"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4404.684982589624,
            "unit": "iter/sec",
            "range": "stddev: 0.00006239146291321517",
            "extra": "mean: 227.03099176279233 usec\nrounds: 1821"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19543.55751405885,
            "unit": "iter/sec",
            "range": "stddev: 0.000005273255290915882",
            "extra": "mean: 51.16775690815964 usec\nrounds: 8034"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1891518.2816613368,
            "unit": "iter/sec",
            "range": "stddev: 8.227348022362892e-8",
            "extra": "mean: 528.6758313124509 nsec\nrounds: 184129"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 242060.99338109206,
            "unit": "iter/sec",
            "range": "stddev: 7.424080073543875e-7",
            "extra": "mean: 4.131190184887147 usec\nrounds: 36454"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1764589.4672307058,
            "unit": "iter/sec",
            "range": "stddev: 5.347215044200841e-8",
            "extra": "mean: 566.7040513221937 nsec\nrounds: 68743"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1291876.9041598192,
            "unit": "iter/sec",
            "range": "stddev: 1.1938016249571582e-7",
            "extra": "mean: 774.067557659712 nsec\nrounds: 162814"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 279361.0524345405,
            "unit": "iter/sec",
            "range": "stddev: 6.317302170382283e-7",
            "extra": "mean: 3.5795970529367853 usec\nrounds: 54630"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 147258.76770755125,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010109664519919922",
            "extra": "mean: 6.790767134395361 usec\nrounds: 30932"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64762.39854122342,
            "unit": "iter/sec",
            "range": "stddev: 0.00037695029421434963",
            "extra": "mean: 15.441058739717104 usec\nrounds: 23153"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8055374.4230166,
            "unit": "iter/sec",
            "range": "stddev: 1.066045956219878e-8",
            "extra": "mean: 124.1407223907214 nsec\nrounds: 80815"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "713f83daefb9d9288319b675cbff116e64705277",
          "message": "Merge pull request #24 from nikolasil/add-create-release-workflow\n\nAdd create release workflow",
          "timestamp": "2026-02-15T15:45:35-05:00",
          "tree_id": "fc40457edf775858e1c67d28a8275ed880abcfa5",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/713f83daefb9d9288319b675cbff116e64705277"
        },
        "date": 1771188488985,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 202347.42088548472,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016776568056232436",
            "extra": "mean: 4.941995285257102 usec\nrounds: 16756"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 200263.79050199754,
            "unit": "iter/sec",
            "range": "stddev: 8.583137977381023e-7",
            "extra": "mean: 4.993413924171307 usec\nrounds: 34731"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 202303.86305678877,
            "unit": "iter/sec",
            "range": "stddev: 8.643980998416024e-7",
            "extra": "mean: 4.943059340983962 usec\nrounds: 37175"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 303063.7641635432,
            "unit": "iter/sec",
            "range": "stddev: 7.36273567220471e-7",
            "extra": "mean: 3.2996356484913423 usec\nrounds: 43856"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 419171.15932467877,
            "unit": "iter/sec",
            "range": "stddev: 5.821796314817649e-7",
            "extra": "mean: 2.3856603150156777 usec\nrounds: 91997"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 432166.7673014881,
            "unit": "iter/sec",
            "range": "stddev: 5.626665799781837e-7",
            "extra": "mean: 2.31392155913363 usec\nrounds: 94976"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5720440.948052431,
            "unit": "iter/sec",
            "range": "stddev: 4.0149766734826344e-8",
            "extra": "mean: 174.8116987975354 nsec\nrounds: 186220"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 52526.849756910495,
            "unit": "iter/sec",
            "range": "stddev: 0.00000223969231359428",
            "extra": "mean: 19.037882618659022 usec\nrounds: 13503"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 90479.17723802842,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014295247453135567",
            "extra": "mean: 11.052266726179953 usec\nrounds: 39205"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20155.231761576946,
            "unit": "iter/sec",
            "range": "stddev: 0.0000059362164051123396",
            "extra": "mean: 49.614909509815526 usec\nrounds: 5426"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 41536.17133959511,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031826131405538156",
            "extra": "mean: 24.07540145730119 usec\nrounds: 14410"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9031.21334754693,
            "unit": "iter/sec",
            "range": "stddev: 0.0000054792117138173694",
            "extra": "mean: 110.72709297379419 usec\nrounds: 4711"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4476.522753760009,
            "unit": "iter/sec",
            "range": "stddev: 0.0000649408695436973",
            "extra": "mean: 223.38767275561378 usec\nrounds: 1916"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19055.865373476725,
            "unit": "iter/sec",
            "range": "stddev: 0.0000059465787668571425",
            "extra": "mean: 52.477280900182535 usec\nrounds: 8398"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1904881.2176179425,
            "unit": "iter/sec",
            "range": "stddev: 8.484397024177078e-8",
            "extra": "mean: 524.9671164538851 nsec\nrounds: 178222"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 239558.61244391877,
            "unit": "iter/sec",
            "range": "stddev: 8.207240318041683e-7",
            "extra": "mean: 4.1743437641345595 usec\nrounds: 33171"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1768358.0574691969,
            "unit": "iter/sec",
            "range": "stddev: 5.526048107601468e-8",
            "extra": "mean: 565.4963347361935 nsec\nrounds: 66721"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1102117.3800292776,
            "unit": "iter/sec",
            "range": "stddev: 3.8688040233420406e-7",
            "extra": "mean: 907.3443701372672 nsec\nrounds: 193051"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 279811.04101231194,
            "unit": "iter/sec",
            "range": "stddev: 7.397096831699454e-7",
            "extra": "mean: 3.573840390222483 usec\nrounds: 52785"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 146423.48681112434,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010288502963401222",
            "extra": "mean: 6.829505441909926 usec\nrounds: 19203"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 59706.14858061177,
            "unit": "iter/sec",
            "range": "stddev: 0.0005062480702104644",
            "extra": "mean: 16.748693790721706 usec\nrounds: 20437"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8423919.76451283,
            "unit": "iter/sec",
            "range": "stddev: 1.1430978786194777e-8",
            "extra": "mean: 118.70958270672492 nsec\nrounds: 81813"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "b6c61f2a971bf77c97ba4cffb574930d0532f365",
          "message": "Merge pull request #25 from nikolasil/add-create-release-workflow\n\nfix: update homebrew formula URL version and fix summary step",
          "timestamp": "2026-02-15T17:55:49-05:00",
          "tree_id": "2957e0737af6a4bf673909ef625dea95c4da6102",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/b6c61f2a971bf77c97ba4cffb574930d0532f365"
        },
        "date": 1771196294713,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 205697.74437193715,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015627737126931252",
            "extra": "mean: 4.861502021100566 usec\nrounds: 17812"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 209233.35248185848,
            "unit": "iter/sec",
            "range": "stddev: 8.66831997657079e-7",
            "extra": "mean: 4.779352756806326 usec\nrounds: 38287"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 205448.86263961522,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010841879353950474",
            "extra": "mean: 4.86739126784135 usec\nrounds: 38112"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 312711.97616865975,
            "unit": "iter/sec",
            "range": "stddev: 6.483703346590189e-7",
            "extra": "mean: 3.197830835428748 usec\nrounds: 45104"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 439545.629514064,
            "unit": "iter/sec",
            "range": "stddev: 5.742838326371462e-7",
            "extra": "mean: 2.275076653828959 usec\nrounds: 95429"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 446671.0047218826,
            "unit": "iter/sec",
            "range": "stddev: 5.551118806057648e-7",
            "extra": "mean: 2.2387842269337472 usec\nrounds: 100513"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5836094.994661243,
            "unit": "iter/sec",
            "range": "stddev: 2.3249818442948622e-8",
            "extra": "mean: 171.34745080654017 nsec\nrounds: 198808"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 50719.22376131256,
            "unit": "iter/sec",
            "range": "stddev: 0.000002245954779224789",
            "extra": "mean: 19.71639007540917 usec\nrounds: 12595"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 89260.07741063986,
            "unit": "iter/sec",
            "range": "stddev: 0.000001407539325575372",
            "extra": "mean: 11.20321681326258 usec\nrounds: 39112"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20621.316631040758,
            "unit": "iter/sec",
            "range": "stddev: 0.0000057873968395247275",
            "extra": "mean: 48.493508823521225 usec\nrounds: 6120"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42930.04407986162,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026799621629224544",
            "extra": "mean: 23.29371006793579 usec\nrounds: 16935"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9135.920932906882,
            "unit": "iter/sec",
            "range": "stddev: 0.0000064045246778862555",
            "extra": "mean: 109.45804011920433 usec\nrounds: 4362"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4468.770436456921,
            "unit": "iter/sec",
            "range": "stddev: 0.00006014636537104721",
            "extra": "mean: 223.77520040900853 usec\nrounds: 1956"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19652.676366302552,
            "unit": "iter/sec",
            "range": "stddev: 0.000005714618174886038",
            "extra": "mean: 50.88365479394193 usec\nrounds: 9658"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1560146.5769688396,
            "unit": "iter/sec",
            "range": "stddev: 2.5380093629716755e-7",
            "extra": "mean: 640.9654161744655 nsec\nrounds: 179824"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 240546.94569555338,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010905736172858951",
            "extra": "mean: 4.157192672342817 usec\nrounds: 34172"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1779384.9744904952,
            "unit": "iter/sec",
            "range": "stddev: 5.3090399904641e-8",
            "extra": "mean: 561.9919322327924 nsec\nrounds: 69945"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1300895.393319403,
            "unit": "iter/sec",
            "range": "stddev: 1.3286475214905463e-7",
            "extra": "mean: 768.7013153672688 nsec\nrounds: 157928"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 286673.6343714333,
            "unit": "iter/sec",
            "range": "stddev: 6.87419792914076e-7",
            "extra": "mean: 3.488287306897341 usec\nrounds: 53462"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 145748.97673224215,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011058661030733599",
            "extra": "mean: 6.861111634678003 usec\nrounds: 26103"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64298.02330236112,
            "unit": "iter/sec",
            "range": "stddev: 0.0003950841639139377",
            "extra": "mean: 15.552577647644084 usec\nrounds: 22029"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8132354.289545932,
            "unit": "iter/sec",
            "range": "stddev: 1.0421853731636441e-8",
            "extra": "mean: 122.96562156499257 nsec\nrounds: 81150"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "19e5c93795896cdb71cf34ce25dbc5cfe62585db",
          "message": "Merge pull request #26 from nikolasil/add-create-release-workflow\n\nfix: combine version bump, Homebrew update, and tag into single atomi…",
          "timestamp": "2026-02-15T18:17:03-05:00",
          "tree_id": "fe89395b665a8e87938bbacf7e25796502819a99",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/19e5c93795896cdb71cf34ce25dbc5cfe62585db"
        },
        "date": 1771197593327,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 201948.58203883917,
            "unit": "iter/sec",
            "range": "stddev: 0.000001778806655363222",
            "extra": "mean: 4.951755490948077 usec\nrounds: 15480"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 205845.50839034485,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011196031452645709",
            "extra": "mean: 4.858012243355342 usec\nrounds: 36428"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 204493.08701924814,
            "unit": "iter/sec",
            "range": "stddev: 7.351737256145682e-7",
            "extra": "mean: 4.890140857944376 usec\nrounds: 38301"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 304607.49057681405,
            "unit": "iter/sec",
            "range": "stddev: 6.49000321636615e-7",
            "extra": "mean: 3.282913358783034 usec\nrounds: 44540"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 435887.75021543785,
            "unit": "iter/sec",
            "range": "stddev: 5.987350048477117e-7",
            "extra": "mean: 2.294168623701284 usec\nrounds: 105175"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 450171.026528539,
            "unit": "iter/sec",
            "range": "stddev: 5.197420252246429e-7",
            "extra": "mean: 2.221377967639159 usec\nrounds: 106861"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5830072.358438981,
            "unit": "iter/sec",
            "range": "stddev: 3.244208722764683e-8",
            "extra": "mean: 171.52445776301852 nsec\nrounds: 179534"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 51565.277941335444,
            "unit": "iter/sec",
            "range": "stddev: 0.000001930300110694295",
            "extra": "mean: 19.392894597362115 usec\nrounds: 13586"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 86518.01281555044,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012920015096022334",
            "extra": "mean: 11.558286736565725 usec\nrounds: 39688"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20734.598520812666,
            "unit": "iter/sec",
            "range": "stddev: 0.000005313920704787399",
            "extra": "mean: 48.22856825495005 usec\nrounds: 5897"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42709.74027862669,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026793439975231607",
            "extra": "mean: 23.413862820899237 usec\nrounds: 16832"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9099.39284007075,
            "unit": "iter/sec",
            "range": "stddev: 0.0000057374586978445275",
            "extra": "mean: 109.89744234322175 usec\nrounds: 4336"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4503.937318873005,
            "unit": "iter/sec",
            "range": "stddev: 0.00006248577102200713",
            "extra": "mean: 222.02795669683616 usec\nrounds: 1986"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19784.585604192675,
            "unit": "iter/sec",
            "range": "stddev: 0.00000563393536373264",
            "extra": "mean: 50.544399564683516 usec\nrounds: 9648"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1902143.174408349,
            "unit": "iter/sec",
            "range": "stddev: 7.896505971731583e-8",
            "extra": "mean: 525.7227812575546 nsec\nrounds: 186602"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 243672.8181832476,
            "unit": "iter/sec",
            "range": "stddev: 8.422581469672511e-7",
            "extra": "mean: 4.103863563674044 usec\nrounds: 34419"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1751582.4003924285,
            "unit": "iter/sec",
            "range": "stddev: 6.56394129168901e-8",
            "extra": "mean: 570.9123360544901 nsec\nrounds: 69459"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1258058.5246121273,
            "unit": "iter/sec",
            "range": "stddev: 1.2372614456177435e-7",
            "extra": "mean: 794.8755804571734 nsec\nrounds: 153328"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 283637.7778775741,
            "unit": "iter/sec",
            "range": "stddev: 6.474878564462758e-7",
            "extra": "mean: 3.5256234465058736 usec\nrounds: 54072"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 145617.67936217465,
            "unit": "iter/sec",
            "range": "stddev: 8.960313437837509e-7",
            "extra": "mean: 6.86729801202805 usec\nrounds: 21932"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 64986.90351466393,
            "unit": "iter/sec",
            "range": "stddev: 0.00039763323843017257",
            "extra": "mean: 15.387715769137326 usec\nrounds: 23305"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8128107.313337165,
            "unit": "iter/sec",
            "range": "stddev: 1.034870316960167e-8",
            "extra": "mean: 123.02987170948336 nsec\nrounds: 79663"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "34923640+nikolasil@users.noreply.github.com",
            "name": "Nikolas Iliopoulos",
            "username": "nikolasil"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "4096cba46f9335921d287e572991a231f6d3044a",
          "message": "Merge pull request #27 from nikolasil/feature/docs-update-and-bookmarks\n\nFeature/docs update and bookmarks",
          "timestamp": "2026-02-15T20:01:06-05:00",
          "tree_id": "2ce7830072457d31dc30befc74c00c3b9d21fb23",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/4096cba46f9335921d287e572991a231f6d3044a"
        },
        "date": 1771203819359,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 199927.92324354197,
            "unit": "iter/sec",
            "range": "stddev: 0.000001168929942064372",
            "extra": "mean: 5.001802568527914 usec\nrounds: 24216"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 199057.77394550678,
            "unit": "iter/sec",
            "range": "stddev: 7.744760001144054e-7",
            "extra": "mean: 5.023667150391 usec\nrounds: 40658"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 198714.0791278322,
            "unit": "iter/sec",
            "range": "stddev: 8.045048697576517e-7",
            "extra": "mean: 5.0323560584587606 usec\nrounds: 42420"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 303090.67580515763,
            "unit": "iter/sec",
            "range": "stddev: 6.207621539179456e-7",
            "extra": "mean: 3.2993426714415057 usec\nrounds: 51081"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 427876.6523016834,
            "unit": "iter/sec",
            "range": "stddev: 5.492773558585955e-7",
            "extra": "mean: 2.337122146349152 usec\nrounds: 105742"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 432370.20652097336,
            "unit": "iter/sec",
            "range": "stddev: 5.195554605478354e-7",
            "extra": "mean: 2.312832810674924 usec\nrounds: 107782"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5796157.872651394,
            "unit": "iter/sec",
            "range": "stddev: 2.822721072733624e-8",
            "extra": "mean: 172.52808187271327 nsec\nrounds: 199641"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 50002.98822575384,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020986408035418415",
            "extra": "mean: 19.99880478113014 usec\nrounds: 13595"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 87361.54176407636,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012619467960039055",
            "extra": "mean: 11.446684431240277 usec\nrounds: 38391"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20723.315946154984,
            "unit": "iter/sec",
            "range": "stddev: 0.0000052639202016583975",
            "extra": "mean: 48.25482575270685 usec\nrounds: 7805"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42956.923618117995,
            "unit": "iter/sec",
            "range": "stddev: 0.000002577364987518479",
            "extra": "mean: 23.279134439185697 usec\nrounds: 17242"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9179.942504710609,
            "unit": "iter/sec",
            "range": "stddev: 0.000004827786426267549",
            "extra": "mean: 108.93314413318586 usec\nrounds: 4926"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 4497.660016741616,
            "unit": "iter/sec",
            "range": "stddev: 0.00006485641140359856",
            "extra": "mean: 222.33783707032217 usec\nrounds: 2007"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 20001.473218181316,
            "unit": "iter/sec",
            "range": "stddev: 0.00000509232894730165",
            "extra": "mean: 49.996317225823205 usec\nrounds: 9747"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1880896.647974127,
            "unit": "iter/sec",
            "range": "stddev: 7.598075301341199e-8",
            "extra": "mean: 531.6613228467808 nsec\nrounds: 168606"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 243356.13992714905,
            "unit": "iter/sec",
            "range": "stddev: 6.798843864873629e-7",
            "extra": "mean: 4.109203902968543 usec\nrounds: 37356"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1739883.5910409798,
            "unit": "iter/sec",
            "range": "stddev: 5.332562594639288e-8",
            "extra": "mean: 574.7510955039662 nsec\nrounds: 70196"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1257010.89306477,
            "unit": "iter/sec",
            "range": "stddev: 1.3021949558059392e-7",
            "extra": "mean: 795.5380542181045 nsec\nrounds: 178540"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 284360.26002885145,
            "unit": "iter/sec",
            "range": "stddev: 6.870699626087566e-7",
            "extra": "mean: 3.5166657953489673 usec\nrounds: 62740"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 148065.25826786627,
            "unit": "iter/sec",
            "range": "stddev: 9.482183638894585e-7",
            "extra": "mean: 6.753778784425517 usec\nrounds: 29912"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 78759.48343908881,
            "unit": "iter/sec",
            "range": "stddev: 0.00005319494289056144",
            "extra": "mean: 12.696883680977699 usec\nrounds: 23874"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8016328.005925879,
            "unit": "iter/sec",
            "range": "stddev: 1.0538281295411063e-8",
            "extra": "mean: 124.74539455740172 nsec\nrounds: 79152"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "9d845b325c1de650df2e4ccf778e20aeb161dad8",
          "message": "fix(ci): lower coverage threshold and ignore benchmark tests\n\nCoverage was 76% with 90% threshold. Benchmark tests inflate coverage\nnumbers and run separately. Setting threshold to 75% and ignoring\ntests/benchmark directory for coverage calculation.",
          "timestamp": "2026-05-19T17:27:48-04:00",
          "tree_id": "bc0cd3921c43cd84db8025c458915515b1755628",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/9d845b325c1de650df2e4ccf778e20aeb161dad8"
        },
        "date": 1779226223133,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 182775.48492420357,
            "unit": "iter/sec",
            "range": "stddev: 0.000002221945044561327",
            "extra": "mean: 5.471193253376933 usec\nrounds: 6344"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 184555.71696342368,
            "unit": "iter/sec",
            "range": "stddev: 7.921720186343739e-7",
            "extra": "mean: 5.4184178981471804 usec\nrounds: 15901"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 170984.41792444434,
            "unit": "iter/sec",
            "range": "stddev: 9.182535160304189e-7",
            "extra": "mean: 5.848486149433138 usec\nrounds: 15559"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 508387.2988722841,
            "unit": "iter/sec",
            "range": "stddev: 4.219777062327886e-7",
            "extra": "mean: 1.9670042942029078 usec\nrounds: 21191"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 510204.1578464416,
            "unit": "iter/sec",
            "range": "stddev: 5.703041285277805e-7",
            "extra": "mean: 1.9599997072171536 usec\nrounds: 40991"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 525221.966422862,
            "unit": "iter/sec",
            "range": "stddev: 6.029586373289965e-7",
            "extra": "mean: 1.9039569247469155 usec\nrounds: 43041"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5990076.477032591,
            "unit": "iter/sec",
            "range": "stddev: 2.6366181484462844e-8",
            "extra": "mean: 166.94277674652767 nsec\nrounds: 95658"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 61326.862407602755,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015639596933315115",
            "extra": "mean: 16.30606818515517 usec\nrounds: 6541"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 102931.50433234859,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010426850151828299",
            "extra": "mean: 9.71519853407726 usec\nrounds: 20329"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 28411.416323550024,
            "unit": "iter/sec",
            "range": "stddev: 0.0000034428733956688886",
            "extra": "mean: 35.19711895429539 usec\nrounds: 3060"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43190.16856095626,
            "unit": "iter/sec",
            "range": "stddev: 0.000002118808881838248",
            "extra": "mean: 23.153417393790768 usec\nrounds: 6876"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9157.862149834058,
            "unit": "iter/sec",
            "range": "stddev: 0.000004356077291521512",
            "extra": "mean: 109.19579085585167 usec\nrounds: 2209"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 2912.7600911470972,
            "unit": "iter/sec",
            "range": "stddev: 0.00007658925145402955",
            "extra": "mean: 343.3169807013464 usec\nrounds: 570"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 29941.22412404258,
            "unit": "iter/sec",
            "range": "stddev: 0.000003973634260619725",
            "extra": "mean: 33.39876806162402 usec\nrounds: 4803"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 2056168.08328202,
            "unit": "iter/sec",
            "range": "stddev: 8.51962983599187e-8",
            "extra": "mean: 486.3415632849515 nsec\nrounds: 90761"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 239280.2404662934,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013346816077730688",
            "extra": "mean: 4.1792000795856215 usec\nrounds: 10066"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1498178.0434439324,
            "unit": "iter/sec",
            "range": "stddev: 4.97888138903429e-7",
            "extra": "mean: 667.4774098953238 nsec\nrounds: 96768"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1415587.8894284759,
            "unit": "iter/sec",
            "range": "stddev: 1.298879211485875e-7",
            "extra": "mean: 706.4202847933145 nsec\nrounds: 81580"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 284905.7011280926,
            "unit": "iter/sec",
            "range": "stddev: 6.448546277497722e-7",
            "extra": "mean: 3.509933272800335 usec\nrounds: 17624"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 147460.6873792056,
            "unit": "iter/sec",
            "range": "stddev: 9.085074465280121e-7",
            "extra": "mean: 6.78146845625661 usec\nrounds: 8829"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 79258.55346219438,
            "unit": "iter/sec",
            "range": "stddev: 0.000043129905094720085",
            "extra": "mean: 12.616934782653976 usec\nrounds: 9982"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8727842.764391966,
            "unit": "iter/sec",
            "range": "stddev: 4.965362672078837e-8",
            "extra": "mean: 114.57584961079014 nsec\nrounds: 41160"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "403eed9c6738a543daa394d746e5ad1703c94ab2",
          "message": "fix(docker): clean up container before running tests in CI\n\nRemove any existing container with the same name before creating a new one to avoid conflicts.",
          "timestamp": "2026-05-19T17:31:33-04:00",
          "tree_id": "79c4f98a089b1a9ac7549e4ad2464ecb0dd3ed09",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/403eed9c6738a543daa394d746e5ad1703c94ab2"
        },
        "date": 1779226446107,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 184770.57519289717,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017337035659009973",
            "extra": "mean: 5.412117156403382 usec\nrounds: 8271"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 181616.81948997395,
            "unit": "iter/sec",
            "range": "stddev: 9.895919792804537e-7",
            "extra": "mean: 5.5060979638794105 usec\nrounds: 17680"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 173399.2924145198,
            "unit": "iter/sec",
            "range": "stddev: 9.051144221146718e-7",
            "extra": "mean: 5.7670362207098815 usec\nrounds: 18056"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 507139.1933733203,
            "unit": "iter/sec",
            "range": "stddev: 4.7087865934886227e-7",
            "extra": "mean: 1.971845231184627 usec\nrounds: 27680"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 518853.07603992155,
            "unit": "iter/sec",
            "range": "stddev: 5.42986742788856e-7",
            "extra": "mean: 1.9273278817818131 usec\nrounds: 52095"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 487458.5129534541,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010237280704147304",
            "extra": "mean: 2.051456633593528 usec\nrounds: 49762"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5349119.8605705965,
            "unit": "iter/sec",
            "range": "stddev: 4.738144031743773e-8",
            "extra": "mean: 186.94664282457123 nsec\nrounds: 68644"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 57229.64640043703,
            "unit": "iter/sec",
            "range": "stddev: 0.000001912495477850543",
            "extra": "mean: 17.47346109746999 usec\nrounds: 7326"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 100531.64392736957,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013841992160177912",
            "extra": "mean: 9.947116757808748 usec\nrounds: 20838"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 20190.933386952,
            "unit": "iter/sec",
            "range": "stddev: 0.000005819255257419533",
            "extra": "mean: 49.527180385144085 usec\nrounds: 2855"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 37639.99892941349,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036499994148180386",
            "extra": "mean: 26.56748215841626 usec\nrounds: 6894"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 8847.924589918595,
            "unit": "iter/sec",
            "range": "stddev: 0.000006898237450897494",
            "extra": "mean: 113.0208547594776 usec\nrounds: 2038"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 2558.127380770963,
            "unit": "iter/sec",
            "range": "stddev: 0.0000636265138637593",
            "extra": "mean: 390.91094818688117 usec\nrounds: 579"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 19930.770999110227,
            "unit": "iter/sec",
            "range": "stddev: 0.00000977781522574285",
            "extra": "mean: 50.17367366493966 usec\nrounds: 4906"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1947679.148935584,
            "unit": "iter/sec",
            "range": "stddev: 9.508907447167767e-8",
            "extra": "mean: 513.4315888458772 nsec\nrounds: 91895"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 246507.6082795296,
            "unit": "iter/sec",
            "range": "stddev: 7.723385178797538e-7",
            "extra": "mean: 4.056669921790165 usec\nrounds: 17920"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1767396.8410243932,
            "unit": "iter/sec",
            "range": "stddev: 5.516856980248785e-8",
            "extra": "mean: 565.8038855724054 nsec\nrounds: 34538"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1296723.881292085,
            "unit": "iter/sec",
            "range": "stddev: 1.1511712179546675e-7",
            "extra": "mean: 771.1741986301582 nsec\nrounds: 80103"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 285787.31653550756,
            "unit": "iter/sec",
            "range": "stddev: 8.163877345166302e-7",
            "extra": "mean: 3.4991056010554455 usec\nrounds: 26477"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 147473.27351034412,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011072782570240784",
            "extra": "mean: 6.7808896906994995 usec\nrounds: 12610"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 79841.31128056042,
            "unit": "iter/sec",
            "range": "stddev: 0.00003474662199020485",
            "extra": "mean: 12.524844393975751 usec\nrounds: 11889"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 7957919.826381738,
            "unit": "iter/sec",
            "range": "stddev: 1.1726759855980241e-8",
            "extra": "mean: 125.66097947918259 nsec\nrounds: 39327"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "cc220f142b7a88e05925658bf578d95da38ba904",
          "message": "fix(ci): exclude ci_excluded tests from mutation testing\n\nMutation tests are failing because ci_excluded tests (like test_http_server.py)\ndon't work in the CI environment. Exclude them from mutation testing.",
          "timestamp": "2026-05-19T17:35:18-04:00",
          "tree_id": "e4e9be0ab3a0d622dca04a681dbce904fc2d8860",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/cc220f142b7a88e05925658bf578d95da38ba904"
        },
        "date": 1779226669120,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 199131.79440740027,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014218787485139047",
            "extra": "mean: 5.0217997732402155 usec\nrounds: 8820"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 200108.059805415,
            "unit": "iter/sec",
            "range": "stddev: 8.022383782854513e-7",
            "extra": "mean: 4.997299963691615 usec\nrounds: 16522"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 161317.65300701547,
            "unit": "iter/sec",
            "range": "stddev: 0.000002113530422114485",
            "extra": "mean: 6.198949596399791 usec\nrounds: 17221"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 541253.6675749997,
            "unit": "iter/sec",
            "range": "stddev: 6.584054546565839e-7",
            "extra": "mean: 1.847562538431083 usec\nrounds: 27655"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 544538.8028344193,
            "unit": "iter/sec",
            "range": "stddev: 3.4644744331774797e-7",
            "extra": "mean: 1.8364164221077102 usec\nrounds: 48045"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 565729.5344548906,
            "unit": "iter/sec",
            "range": "stddev: 3.774328522859913e-7",
            "extra": "mean: 1.7676291215086573 usec\nrounds: 47889"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 6203230.680483209,
            "unit": "iter/sec",
            "range": "stddev: 1.4315306644210768e-8",
            "extra": "mean: 161.20632159404133 nsec\nrounds: 96377"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 64758.96713263507,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016372681715246057",
            "extra": "mean: 15.441876921104464 usec\nrounds: 7873"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 107592.57492259744,
            "unit": "iter/sec",
            "range": "stddev: 9.896704011658384e-7",
            "extra": "mean: 9.294321664105578 usec\nrounds: 19253"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 27102.671034283223,
            "unit": "iter/sec",
            "range": "stddev: 0.00000266687835968115",
            "extra": "mean: 36.896732382393644 usec\nrounds: 3576"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43281.33790637588,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015860960621134046",
            "extra": "mean: 23.104646214106236 usec\nrounds: 6894"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 10523.33753013084,
            "unit": "iter/sec",
            "range": "stddev: 0.000005044865982256788",
            "extra": "mean: 95.02688639766235 usec\nrounds: 2007"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 2866.3504102800844,
            "unit": "iter/sec",
            "range": "stddev: 0.00010405145990169737",
            "extra": "mean: 348.8756979654436 usec\nrounds: 639"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 28593.90820181222,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028429854611697452",
            "extra": "mean: 34.97248410193267 usec\nrounds: 4749"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1996976.025080997,
            "unit": "iter/sec",
            "range": "stddev: 5.062073415739087e-8",
            "extra": "mean: 500.7571385136885 nsec\nrounds: 88779"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 249457.48256752483,
            "unit": "iter/sec",
            "range": "stddev: 9.462548876253758e-7",
            "extra": "mean: 4.008699156696225 usec\nrounds: 17195"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1526664.2262724675,
            "unit": "iter/sec",
            "range": "stddev: 2.689739786296197e-7",
            "extra": "mean: 655.0228811227332 nsec\nrounds: 87889"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1359593.9991241556,
            "unit": "iter/sec",
            "range": "stddev: 7.658882853869187e-8",
            "extra": "mean: 735.5136905901161 nsec\nrounds: 79215"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 305592.31786594127,
            "unit": "iter/sec",
            "range": "stddev: 8.874234336382345e-7",
            "extra": "mean: 3.2723335684069284 usec\nrounds: 26945"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 157916.26365100013,
            "unit": "iter/sec",
            "range": "stddev: 6.089517788027924e-7",
            "extra": "mean: 6.332469986815489 usec\nrounds: 14377"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 83810.53221528776,
            "unit": "iter/sec",
            "range": "stddev: 0.00007073926959991478",
            "extra": "mean: 11.931674618546229 usec\nrounds: 8258"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8669993.145666968,
            "unit": "iter/sec",
            "range": "stddev: 1.86058315631449e-8",
            "extra": "mean: 115.34034493437284 nsec\nrounds: 41979"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "8b1fd20fed49f4b12628256016b4ba5dbc083690",
          "message": "fix(ci): exclude more tests from mutation testing\n\nIgnore test_http_server.py and test_mutations.py from mutation testing\nas they have environment-specific issues in CI.",
          "timestamp": "2026-05-19T17:39:35-04:00",
          "tree_id": "5c5dc3b47609155862ef7dd1ecc7ada045317e96",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/8b1fd20fed49f4b12628256016b4ba5dbc083690"
        },
        "date": 1779226927422,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 184762.474589477,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019413048308996713",
            "extra": "mean: 5.412354441679221 usec\nrounds: 6743"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 182912.1775110021,
            "unit": "iter/sec",
            "range": "stddev: 8.741619908436861e-7",
            "extra": "mean: 5.467104561367164 usec\nrounds: 13724"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 172575.37563279335,
            "unit": "iter/sec",
            "range": "stddev: 7.677587069774137e-7",
            "extra": "mean: 5.794569453105549 usec\nrounds: 14463"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 508645.7878568941,
            "unit": "iter/sec",
            "range": "stddev: 4.797219010666997e-7",
            "extra": "mean: 1.966004681201345 usec\nrounds: 23071"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 514151.92987339303,
            "unit": "iter/sec",
            "range": "stddev: 5.448703736268389e-7",
            "extra": "mean: 1.944950396755769 usec\nrounds: 47638"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 518527.65548916766,
            "unit": "iter/sec",
            "range": "stddev: 5.229010095167477e-7",
            "extra": "mean: 1.928537445233508 usec\nrounds: 47683"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5866271.657866364,
            "unit": "iter/sec",
            "range": "stddev: 2.616785064301309e-8",
            "extra": "mean: 170.46602311011023 nsec\nrounds: 99266"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 59707.12751391005,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016247526367059736",
            "extra": "mean: 16.74841918608509 usec\nrounds: 6880"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 100584.87780120205,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011643930607143402",
            "extra": "mean: 9.941852312794174 usec\nrounds: 19284"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 28341.355910393282,
            "unit": "iter/sec",
            "range": "stddev: 0.000003953608371918897",
            "extra": "mean: 35.284126954324094 usec\nrounds: 3198"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43126.87097260867,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022507185395059276",
            "extra": "mean: 23.187399814726504 usec\nrounds: 6478"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9284.237430928477,
            "unit": "iter/sec",
            "range": "stddev: 0.000004261634055156636",
            "extra": "mean: 107.70943843688349 usec\nrounds: 1868"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 2908.52176517567,
            "unit": "iter/sec",
            "range": "stddev: 0.00007929843992369029",
            "extra": "mean: 343.81726551721425 usec\nrounds: 580"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 29970.3045092047,
            "unit": "iter/sec",
            "range": "stddev: 0.0000040624646072569344",
            "extra": "mean: 33.366361015547 usec\nrounds: 3781"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 2151102.867953144,
            "unit": "iter/sec",
            "range": "stddev: 7.990439608969015e-8",
            "extra": "mean: 464.8778144912884 nsec\nrounds: 88826"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 245805.0319218763,
            "unit": "iter/sec",
            "range": "stddev: 7.336441008701459e-7",
            "extra": "mean: 4.068264966674189 usec\nrounds: 15451"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1465015.041006326,
            "unit": "iter/sec",
            "range": "stddev: 4.3209645290172703e-7",
            "extra": "mean: 682.5868486053871 nsec\nrounds: 87428"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1390357.8833962616,
            "unit": "iter/sec",
            "range": "stddev: 1.3386947070341889e-7",
            "extra": "mean: 719.2392778450633 nsec\nrounds: 81700"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 287310.0538947756,
            "unit": "iter/sec",
            "range": "stddev: 8.155176656184054e-7",
            "extra": "mean: 3.4805604135462658 usec\nrounds: 24084"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 152595.79294375874,
            "unit": "iter/sec",
            "range": "stddev: 8.934374436542816e-7",
            "extra": "mean: 6.553260615569943 usec\nrounds: 13353"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 76961.52965176747,
            "unit": "iter/sec",
            "range": "stddev: 0.000051728421322515975",
            "extra": "mean: 12.993504735739544 usec\nrounds: 7285"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8486307.603836434,
            "unit": "iter/sec",
            "range": "stddev: 1.1673682570524984e-8",
            "extra": "mean: 117.83687873242914 nsec\nrounds: 40522"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "ed804bf7fbfee10ea0e4d24ffb465442842aa537",
          "message": "fix(scorecard): add required results-file and result-format parameters\n\nThe scorecard action requires these parameters to know where to store results.",
          "timestamp": "2026-05-19T17:44:54-04:00",
          "tree_id": "cb5a2dd3bd3520cae528ca3bcc11383ee000f063",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/ed804bf7fbfee10ea0e4d24ffb465442842aa537"
        },
        "date": 1779227276201,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 236621.89312607484,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016656650552828035",
            "extra": "mean: 4.226151632838085 usec\nrounds: 7472"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 236052.01285813455,
            "unit": "iter/sec",
            "range": "stddev: 4.949473744632418e-7",
            "extra": "mean: 4.236354470745362 usec\nrounds: 18498"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 221684.98997278337,
            "unit": "iter/sec",
            "range": "stddev: 5.723331575230829e-7",
            "extra": "mean: 4.510905317147416 usec\nrounds: 18525"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 644624.0072197578,
            "unit": "iter/sec",
            "range": "stddev: 3.2751176481327434e-7",
            "extra": "mean: 1.551291898533173 usec\nrounds: 26958"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 651596.4830503562,
            "unit": "iter/sec",
            "range": "stddev: 5.266785770856958e-7",
            "extra": "mean: 1.5346921384821515 usec\nrounds: 37283"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 663422.7846343571,
            "unit": "iter/sec",
            "range": "stddev: 4.0628435459639137e-7",
            "extra": "mean: 1.5073344225751097 usec\nrounds: 52329"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 7783272.355114137,
            "unit": "iter/sec",
            "range": "stddev: 1.1464026199843462e-8",
            "extra": "mean: 128.48066396429564 nsec\nrounds: 22161"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 76891.55923450085,
            "unit": "iter/sec",
            "range": "stddev: 0.000002407308761128573",
            "extra": "mean: 13.00532867268616 usec\nrounds: 5078"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 132727.3594096171,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010237524846433491",
            "extra": "mean: 7.5342416548335445 usec\nrounds: 23157"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 36361.751507822824,
            "unit": "iter/sec",
            "range": "stddev: 0.000002840550083875072",
            "extra": "mean: 27.50142549609749 usec\nrounds: 2973"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 55158.57309116897,
            "unit": "iter/sec",
            "range": "stddev: 0.000001445638453987098",
            "extra": "mean: 18.129548027777073 usec\nrounds: 8620"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 11974.585918807468,
            "unit": "iter/sec",
            "range": "stddev: 0.000002960628572243092",
            "extra": "mean: 83.51019457210496 usec\nrounds: 2395"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 3760.4103901126446,
            "unit": "iter/sec",
            "range": "stddev: 0.000050357535947806635",
            "extra": "mean: 265.9284217034739 usec\nrounds: 728"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 38359.641035532186,
            "unit": "iter/sec",
            "range": "stddev: 0.000002597156669126648",
            "extra": "mean: 26.06906563785905 usec\nrounds: 5896"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 2789007.2184630083,
            "unit": "iter/sec",
            "range": "stddev: 3.763853486742015e-8",
            "extra": "mean: 358.55052413636815 nsec\nrounds: 51895"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 312414.83004009904,
            "unit": "iter/sec",
            "range": "stddev: 5.421399434071637e-7",
            "extra": "mean: 3.200872378150705 usec\nrounds: 18069"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 2508788.007183964,
            "unit": "iter/sec",
            "range": "stddev: 6.863772139395916e-8",
            "extra": "mean: 398.5988441974658 nsec\nrounds: 45596"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1851117.3478636097,
            "unit": "iter/sec",
            "range": "stddev: 8.149173486824875e-8",
            "extra": "mean: 540.2142663478944 nsec\nrounds: 87582"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 364760.6493088175,
            "unit": "iter/sec",
            "range": "stddev: 7.011233730711208e-7",
            "extra": "mean: 2.7415237962068915 usec\nrounds: 28660"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 196982.56255480184,
            "unit": "iter/sec",
            "range": "stddev: 6.582446859444856e-7",
            "extra": "mean: 5.07659148622251 usec\nrounds: 10712"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 103339.31152990693,
            "unit": "iter/sec",
            "range": "stddev: 0.000028194131601296915",
            "extra": "mean: 9.676859514499425 usec\nrounds: 11987"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 10829548.995787142,
            "unit": "iter/sec",
            "range": "stddev: 8.841682323475768e-9",
            "extra": "mean: 92.33994881865151 nsec\nrounds: 53340"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "30736f4d7983b6e3ff2e012660f079fd5d0ad094",
          "message": "fix(ci): remove trailing whitespace in security_scan.yml",
          "timestamp": "2026-05-19T18:07:03-04:00",
          "tree_id": "bf97d09cd9a1f4eae09f5f1b8568c0550cdbdcd3",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/30736f4d7983b6e3ff2e012660f079fd5d0ad094"
        },
        "date": 1779228608785,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 183843.46517401334,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017504746714182781",
            "extra": "mean: 5.439410093002055 usec\nrounds: 9254"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 180645.16171787173,
            "unit": "iter/sec",
            "range": "stddev: 9.198516840152455e-7",
            "extra": "mean: 5.535714272612414 usec\nrounds: 10916"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 174400.58770624822,
            "unit": "iter/sec",
            "range": "stddev: 8.916139967794086e-7",
            "extra": "mean: 5.733925631514217 usec\nrounds: 19995"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 523022.73774595524,
            "unit": "iter/sec",
            "range": "stddev: 5.058852638198547e-7",
            "extra": "mean: 1.9119627653467794 usec\nrounds: 30563"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 521385.166084178,
            "unit": "iter/sec",
            "range": "stddev: 4.860868348402236e-7",
            "extra": "mean: 1.9179678768201651 usec\nrounds: 62696"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 536883.2223739855,
            "unit": "iter/sec",
            "range": "stddev: 5.71660670074855e-7",
            "extra": "mean: 1.8626024400207721 usec\nrounds: 43933"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 6083543.123085765,
            "unit": "iter/sec",
            "range": "stddev: 2.332307072571718e-8",
            "extra": "mean: 164.3778929100504 nsec\nrounds: 99404"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 56860.84148974426,
            "unit": "iter/sec",
            "range": "stddev: 0.000001882884784584605",
            "extra": "mean: 17.58679565409466 usec\nrounds: 6719"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 100732.40496740903,
            "unit": "iter/sec",
            "range": "stddev: 0.000001945610875125741",
            "extra": "mean: 9.927292020115473 usec\nrounds: 20978"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 18628.22180274545,
            "unit": "iter/sec",
            "range": "stddev: 0.000011679669903956224",
            "extra": "mean: 53.681989112488374 usec\nrounds: 2480"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 34052.10381691301,
            "unit": "iter/sec",
            "range": "stddev: 0.000008646562457660698",
            "extra": "mean: 29.366761166260734 usec\nrounds: 5933"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 8892.813851755107,
            "unit": "iter/sec",
            "range": "stddev: 0.000006763547909231355",
            "extra": "mean: 112.45034661359043 usec\nrounds: 2259"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 2566.915879327255,
            "unit": "iter/sec",
            "range": "stddev: 0.000025835024796500986",
            "extra": "mean: 389.5725637343765 usec\nrounds: 557"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 20435.953351008917,
            "unit": "iter/sec",
            "range": "stddev: 0.000007306460600813828",
            "extra": "mean: 48.93336673968432 usec\nrounds: 5009"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 2002154.6676677442,
            "unit": "iter/sec",
            "range": "stddev: 8.591900037745387e-8",
            "extra": "mean: 499.46191278262876 nsec\nrounds: 87874"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 244215.9393887565,
            "unit": "iter/sec",
            "range": "stddev: 9.210441469649812e-7",
            "extra": "mean: 4.094736823906259 usec\nrounds: 17456"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1814959.6485999462,
            "unit": "iter/sec",
            "range": "stddev: 6.874331383144211e-8",
            "extra": "mean: 550.9764367331227 nsec\nrounds: 35271"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1317085.921040172,
            "unit": "iter/sec",
            "range": "stddev: 1.2639556459818022e-7",
            "extra": "mean: 759.2519091011684 nsec\nrounds: 80361"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 289708.2403664645,
            "unit": "iter/sec",
            "range": "stddev: 7.337294630821787e-7",
            "extra": "mean: 3.4517485548048503 usec\nrounds: 34254"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 148462.14021600145,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012907492640636153",
            "extra": "mean: 6.735723993639549 usec\nrounds: 13141"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 78979.05565323003,
            "unit": "iter/sec",
            "range": "stddev: 0.00003417214501391175",
            "extra": "mean: 12.661584666074729 usec\nrounds: 13004"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 7925183.958667741,
            "unit": "iter/sec",
            "range": "stddev: 1.1816422272741425e-8",
            "extra": "mean: 126.180036351872 nsec\nrounds: 42366"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "9aec747da55a4b306488dab47677d38ca364abd5",
          "message": "fix(tests): apply ruff-format formatting",
          "timestamp": "2026-05-20T09:39:24-04:00",
          "tree_id": "3d365bf8e64724fdf7d9264b25561f3ccf21eaa8",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/9aec747da55a4b306488dab47677d38ca364abd5"
        },
        "date": 1779284537838,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 181649.31752177732,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025113822986397095",
            "extra": "mean: 5.505112893584713 usec\nrounds: 6732"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 184041.6983552969,
            "unit": "iter/sec",
            "range": "stddev: 7.894392196906688e-7",
            "extra": "mean: 5.433551249181999 usec\nrounds: 16771"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 170703.3975149244,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011813210821788472",
            "extra": "mean: 5.858114217747605 usec\nrounds: 15558"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 506395.9370803474,
            "unit": "iter/sec",
            "range": "stddev: 5.753335528827174e-7",
            "extra": "mean: 1.9747393823211794 usec\nrounds: 22439"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 507449.92344189313,
            "unit": "iter/sec",
            "range": "stddev: 5.716179648016555e-7",
            "extra": "mean: 1.9706377985383765 usec\nrounds: 51256"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 523451.3031455302,
            "unit": "iter/sec",
            "range": "stddev: 5.26732241392069e-7",
            "extra": "mean: 1.9103973836549597 usec\nrounds: 43190"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5804279.791034387,
            "unit": "iter/sec",
            "range": "stddev: 3.660975488273755e-8",
            "extra": "mean: 172.28666363471245 nsec\nrounds: 99861"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 61254.44576145549,
            "unit": "iter/sec",
            "range": "stddev: 0.000001617416457669936",
            "extra": "mean: 16.32534565563325 usec\nrounds: 6871"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 101848.24848774025,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011997149305597483",
            "extra": "mean: 9.818529182859464 usec\nrounds: 20303"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 28501.754543532345,
            "unit": "iter/sec",
            "range": "stddev: 0.000003818072390176614",
            "extra": "mean: 35.08555932837901 usec\nrounds: 2680"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42574.830838352136,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023581847565193933",
            "extra": "mean: 23.48805574346952 usec\nrounds: 6799"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9221.393892575841,
            "unit": "iter/sec",
            "range": "stddev: 0.00000947416219924526",
            "extra": "mean: 108.443475210955 usec\nrounds: 1896"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 2921.3808623463083,
            "unit": "iter/sec",
            "range": "stddev: 0.00002335857948741246",
            "extra": "mean: 342.30387858324286 usec\nrounds: 593"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 30110.87510724285,
            "unit": "iter/sec",
            "range": "stddev: 0.000004086628480203146",
            "extra": "mean: 33.21059240020097 usec\nrounds: 3658"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 2197844.918540453,
            "unit": "iter/sec",
            "range": "stddev: 8.861021705146447e-8",
            "extra": "mean: 454.9911559110736 nsec\nrounds: 89622"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 241481.48030178127,
            "unit": "iter/sec",
            "range": "stddev: 7.757568376924292e-7",
            "extra": "mean: 4.1411043147089055 usec\nrounds: 15760"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1985709.3323682935,
            "unit": "iter/sec",
            "range": "stddev: 6.153469562484529e-8",
            "extra": "mean: 503.5983785236447 nsec\nrounds: 37065"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1409639.7578094834,
            "unit": "iter/sec",
            "range": "stddev: 1.3862135345255765e-7",
            "extra": "mean: 709.4011036933925 nsec\nrounds: 84474"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 285992.3696925129,
            "unit": "iter/sec",
            "range": "stddev: 7.090819266320022e-7",
            "extra": "mean: 3.496596783596564 usec\nrounds: 24002"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 149575.0570461481,
            "unit": "iter/sec",
            "range": "stddev: 9.90915159147487e-7",
            "extra": "mean: 6.685606676328874 usec\nrounds: 9646"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 79146.85931187555,
            "unit": "iter/sec",
            "range": "stddev: 0.00004484447565533071",
            "extra": "mean: 12.634740136175632 usec\nrounds: 10721"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8418484.203123515,
            "unit": "iter/sec",
            "range": "stddev: 1.1507889469419535e-8",
            "extra": "mean: 118.78622990447718 nsec\nrounds: 40991"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "79dd9c1e8adfd8b6db4d87c6686e3a775329c2e8",
          "message": "fix(ci): use codeql-action/init and analyze in codeql.yml",
          "timestamp": "2026-05-20T09:44:15-04:00",
          "tree_id": "3db2583220104bdce217727733628f3424f1fdf7",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/79dd9c1e8adfd8b6db4d87c6686e3a775329c2e8"
        },
        "date": 1779284827937,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 181764.7675689301,
            "unit": "iter/sec",
            "range": "stddev: 0.000002179396530063996",
            "extra": "mean: 5.501616255860878 usec\nrounds: 7505"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 182587.4945698215,
            "unit": "iter/sec",
            "range": "stddev: 8.845111330437366e-7",
            "extra": "mean: 5.47682634211074 usec\nrounds: 17045"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 169007.26860647832,
            "unit": "iter/sec",
            "range": "stddev: 9.282732053584102e-7",
            "extra": "mean: 5.916905280141711 usec\nrounds: 9924"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 511136.28277865885,
            "unit": "iter/sec",
            "range": "stddev: 4.696725206328101e-7",
            "extra": "mean: 1.9564253873032869 usec\nrounds: 28534"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 509222.462982918,
            "unit": "iter/sec",
            "range": "stddev: 5.660640375788685e-7",
            "extra": "mean: 1.9637782554646364 usec\nrounds: 53034"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 521432.00531872164,
            "unit": "iter/sec",
            "range": "stddev: 5.634588247259564e-7",
            "extra": "mean: 1.9177955894532348 usec\nrounds: 51558"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 6213308.019748969,
            "unit": "iter/sec",
            "range": "stddev: 2.3529035719955476e-8",
            "extra": "mean: 160.9448617099788 nsec\nrounds: 97277"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 58387.081565885666,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020935917485517474",
            "extra": "mean: 17.127076284358743 usec\nrounds: 7105"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 97817.28410940173,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013643218074472203",
            "extra": "mean: 10.223142148186925 usec\nrounds: 20753"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 19418.71341704383,
            "unit": "iter/sec",
            "range": "stddev: 0.000009411840011482099",
            "extra": "mean: 51.49671754887214 usec\nrounds: 2758"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 36930.86836122604,
            "unit": "iter/sec",
            "range": "stddev: 0.000003970589017077544",
            "extra": "mean: 27.077619465073468 usec\nrounds: 6843"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 8805.72379174992,
            "unit": "iter/sec",
            "range": "stddev: 0.000010192502454103858",
            "extra": "mean: 113.56249908007558 usec\nrounds: 2174"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 2621.095277722835,
            "unit": "iter/sec",
            "range": "stddev: 0.00002969066342893103",
            "extra": "mean: 381.5198968534955 usec\nrounds: 572"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 20199.881626893188,
            "unit": "iter/sec",
            "range": "stddev: 0.000006082005980174695",
            "extra": "mean: 49.50524059847194 usec\nrounds: 4946"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1951063.8109084605,
            "unit": "iter/sec",
            "range": "stddev: 1.0764301787341128e-7",
            "extra": "mean: 512.5408991796921 nsec\nrounds: 94340"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 245661.7904776025,
            "unit": "iter/sec",
            "range": "stddev: 8.249834289718646e-7",
            "extra": "mean: 4.070637106632877 usec\nrounds: 16396"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1786542.5491504779,
            "unit": "iter/sec",
            "range": "stddev: 6.79184054205136e-8",
            "extra": "mean: 559.7403770067045 nsec\nrounds: 14403"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1301765.4380109846,
            "unit": "iter/sec",
            "range": "stddev: 1.251974354297317e-7",
            "extra": "mean: 768.187548079261 nsec\nrounds: 79720"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 286120.65482691285,
            "unit": "iter/sec",
            "range": "stddev: 8.398090524936418e-7",
            "extra": "mean: 3.4950290485143225 usec\nrounds: 24855"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 147506.16541316174,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011826593257993664",
            "extra": "mean: 6.779377642954927 usec\nrounds: 9885"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 78124.3478492585,
            "unit": "iter/sec",
            "range": "stddev: 0.000041872159225986876",
            "extra": "mean: 12.800106849269415 usec\nrounds: 10585"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8249512.09367385,
            "unit": "iter/sec",
            "range": "stddev: 2.419367169885953e-8",
            "extra": "mean: 121.21929014036301 nsec\nrounds: 40346"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "f3da3ec09cef1fadd523ef39958a2b0b08e89aa1",
          "message": "fix(ci): exclude TestCorruptedDatabaseHandling from CI due to Windows file lock issues",
          "timestamp": "2026-05-20T09:57:41-04:00",
          "tree_id": "1cfc7610124ce79d60a54e97bf87d3fafbd2a2cc",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/f3da3ec09cef1fadd523ef39958a2b0b08e89aa1"
        },
        "date": 1779286467960,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 237049.12807105636,
            "unit": "iter/sec",
            "range": "stddev: 0.000002024150460538631",
            "extra": "mean: 4.21853481654759 usec\nrounds: 7956"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 232396.28001342827,
            "unit": "iter/sec",
            "range": "stddev: 5.644765364639605e-7",
            "extra": "mean: 4.3029948669669675 usec\nrounds: 22209"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 223916.40228661982,
            "unit": "iter/sec",
            "range": "stddev: 6.050381281150301e-7",
            "extra": "mean: 4.465952425941399 usec\nrounds: 16942"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 643280.3716170234,
            "unit": "iter/sec",
            "range": "stddev: 3.4359309188468627e-7",
            "extra": "mean: 1.5545321202421976 usec\nrounds: 25280"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 658637.0804005903,
            "unit": "iter/sec",
            "range": "stddev: 3.6063935776692155e-7",
            "extra": "mean: 1.5182868225271935 usec\nrounds: 65096"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 668779.1481158851,
            "unit": "iter/sec",
            "range": "stddev: 3.914572481107771e-7",
            "extra": "mean: 1.4952619303655703 usec\nrounds: 57584"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 7597207.108498187,
            "unit": "iter/sec",
            "range": "stddev: 8.726488900068502e-9",
            "extra": "mean: 131.6273185288578 nsec\nrounds: 22102"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 78469.99104762865,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010693328841064633",
            "extra": "mean: 12.743725169957436 usec\nrounds: 8387"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 131089.5595730025,
            "unit": "iter/sec",
            "range": "stddev: 8.703186865212627e-7",
            "extra": "mean: 7.62837256649039 usec\nrounds: 26916"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 36574.02004862863,
            "unit": "iter/sec",
            "range": "stddev: 0.000002170183955054912",
            "extra": "mean: 27.34181253989595 usec\nrounds: 3142"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 54568.31867161401,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016214002131279804",
            "extra": "mean: 18.32565166645297 usec\nrounds: 8911"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 11777.816836576743,
            "unit": "iter/sec",
            "range": "stddev: 0.000004007684126119172",
            "extra": "mean: 84.90537880453682 usec\nrounds: 2727"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 3779.5718192354975,
            "unit": "iter/sec",
            "range": "stddev: 0.000013244192026894678",
            "extra": "mean: 264.5802349648888 usec\nrounds: 715"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 38849.62347472117,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026459138777494846",
            "extra": "mean: 25.740275208862293 usec\nrounds: 5385"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 2788605.718942508,
            "unit": "iter/sec",
            "range": "stddev: 4.0220613955480176e-8",
            "extra": "mean: 358.60214773541446 nsec\nrounds: 53568"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 311828.24732917757,
            "unit": "iter/sec",
            "range": "stddev: 5.64253141489071e-7",
            "extra": "mean: 3.2068935658172193 usec\nrounds: 13304"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 2544143.717279533,
            "unit": "iter/sec",
            "range": "stddev: 4.035140801448543e-8",
            "extra": "mean: 393.0595560337786 nsec\nrounds: 46400"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1849242.694497005,
            "unit": "iter/sec",
            "range": "stddev: 7.932460801497092e-8",
            "extra": "mean: 540.761903765152 nsec\nrounds: 89478"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 368042.45232054073,
            "unit": "iter/sec",
            "range": "stddev: 4.7493181528031046e-7",
            "extra": "mean: 2.7170778634228476 usec\nrounds: 28794"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 190756.50601598673,
            "unit": "iter/sec",
            "range": "stddev: 7.083271754917117e-7",
            "extra": "mean: 5.242285156534545 usec\nrounds: 13831"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 102256.13541458307,
            "unit": "iter/sec",
            "range": "stddev: 0.00003316766548833468",
            "extra": "mean: 9.779364298735144 usec\nrounds: 12078"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 10753848.76798594,
            "unit": "iter/sec",
            "range": "stddev: 8.00173560732124e-9",
            "extra": "mean: 92.98996308902146 nsec\nrounds: 49579"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "2013fc3d347dd73bc65a78be4f825e365476d785",
          "message": "fix(ci): exclude hypothesis property tests from CI due to flakiness",
          "timestamp": "2026-05-20T10:25:53-04:00",
          "tree_id": "afcf781082b1eeaf10f2d3c183452826c1e63d8b",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/2013fc3d347dd73bc65a78be4f825e365476d785"
        },
        "date": 1779287362185,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 180062.94581069675,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022636301921490783",
            "extra": "mean: 5.5536134627682765 usec\nrounds: 7725"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 179993.86108248294,
            "unit": "iter/sec",
            "range": "stddev: 9.378722841661559e-7",
            "extra": "mean: 5.555745034780635 usec\nrounds: 17673"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 170582.3378334612,
            "unit": "iter/sec",
            "range": "stddev: 9.105848399806117e-7",
            "extra": "mean: 5.862271631992145 usec\nrounds: 16850"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 505186.50583993504,
            "unit": "iter/sec",
            "range": "stddev: 5.71433488089398e-7",
            "extra": "mean: 1.9794669660413362 usec\nrounds: 27169"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 503776.4374383446,
            "unit": "iter/sec",
            "range": "stddev: 5.587846742687494e-7",
            "extra": "mean: 1.9850074868227365 usec\nrounds: 35930"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 518933.55898644944,
            "unit": "iter/sec",
            "range": "stddev: 5.356596101774e-7",
            "extra": "mean: 1.9270289667778306 usec\nrounds: 54131"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 6088977.347054682,
            "unit": "iter/sec",
            "range": "stddev: 2.4383255440970434e-8",
            "extra": "mean: 164.23119072425712 nsec\nrounds: 88324"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 56681.824192501415,
            "unit": "iter/sec",
            "range": "stddev: 0.000002310325280184629",
            "extra": "mean: 17.64233974904944 usec\nrounds: 7014"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 99218.2118197313,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014305823694572762",
            "extra": "mean: 10.078794826668426 usec\nrounds: 15309"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 19854.158776724493,
            "unit": "iter/sec",
            "range": "stddev: 0.000006270045915845938",
            "extra": "mean: 50.367281295862504 usec\nrounds: 2716"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 37108.69847035839,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037133474789563203",
            "extra": "mean: 26.947859699223294 usec\nrounds: 6650"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 8803.163285106562,
            "unit": "iter/sec",
            "range": "stddev: 0.000007949739952746797",
            "extra": "mean: 113.59553010811783 usec\nrounds: 1943"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 2510.610153981663,
            "unit": "iter/sec",
            "range": "stddev: 0.000027441718768038022",
            "extra": "mean: 398.3095497379653 usec\nrounds: 573"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 20363.63795950053,
            "unit": "iter/sec",
            "range": "stddev: 0.000006670940748790064",
            "extra": "mean: 49.107139008698404 usec\nrounds: 4863"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1539549.746081523,
            "unit": "iter/sec",
            "range": "stddev: 3.4098539027681724e-7",
            "extra": "mean: 649.5405572604651 nsec\nrounds: 93633"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 242798.0533119489,
            "unit": "iter/sec",
            "range": "stddev: 7.887091634870189e-7",
            "extra": "mean: 4.118649166907414 usec\nrounds: 17524"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1688215.6306014787,
            "unit": "iter/sec",
            "range": "stddev: 1.105788546138135e-7",
            "extra": "mean: 592.341393998196 nsec\nrounds: 93458"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1277854.0514706173,
            "unit": "iter/sec",
            "range": "stddev: 1.4561111911204234e-7",
            "extra": "mean: 782.5619826061169 nsec\nrounds: 93110"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 285198.9009714242,
            "unit": "iter/sec",
            "range": "stddev: 7.549763930916261e-7",
            "extra": "mean: 3.506324872199266 usec\nrounds: 26789"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 145292.15811095666,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011884974464392202",
            "extra": "mean: 6.882683917712341 usec\nrounds: 9526"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 76761.59467896717,
            "unit": "iter/sec",
            "range": "stddev: 0.00004461843388976289",
            "extra": "mean: 13.027347909878713 usec\nrounds: 11937"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 7789932.868156806,
            "unit": "iter/sec",
            "range": "stddev: 2.4434247221439024e-8",
            "extra": "mean: 128.37081101019555 nsec\nrounds: 40542"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "0db0f2546bd065a24f640899803fb57aa0214600",
          "message": "fix(ci): exclude all error_recovery tests from CI due to Windows file lock issues",
          "timestamp": "2026-05-20T10:36:27-04:00",
          "tree_id": "fca4d4e561abd307dc50966ebff9ec14b569f66f",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/0db0f2546bd065a24f640899803fb57aa0214600"
        },
        "date": 1779287988266,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 179161.37164588727,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017612344860035473",
            "extra": "mean: 5.5815603040620925 usec\nrounds: 9079"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 180485.50435836555,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010207024390189084",
            "extra": "mean: 5.540611161849518 usec\nrounds: 19710"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 173469.09519486054,
            "unit": "iter/sec",
            "range": "stddev: 9.235610792437873e-7",
            "extra": "mean: 5.764715604682692 usec\nrounds: 19821"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 517630.954332407,
            "unit": "iter/sec",
            "range": "stddev: 6.23777458298877e-7",
            "extra": "mean: 1.9318782843844964 usec\nrounds: 32921"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 521921.8637341035,
            "unit": "iter/sec",
            "range": "stddev: 5.350686012141654e-7",
            "extra": "mean: 1.9159956106177927 usec\nrounds: 59917"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 533906.2840365766,
            "unit": "iter/sec",
            "range": "stddev: 5.368511738458581e-7",
            "extra": "mean: 1.8729878817674537 usec\nrounds: 60570"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5932198.345915016,
            "unit": "iter/sec",
            "range": "stddev: 2.4474465480640475e-8",
            "extra": "mean: 168.57157190105897 nsec\nrounds: 99404"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 57631.55504116083,
            "unit": "iter/sec",
            "range": "stddev: 0.000002074797854454701",
            "extra": "mean: 17.351605371151162 usec\nrounds: 7559"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 99195.1839061468,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013751088786086268",
            "extra": "mean: 10.081134593652719 usec\nrounds: 21264"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 19907.313775004786,
            "unit": "iter/sec",
            "range": "stddev: 0.000006456279381252156",
            "extra": "mean: 50.23279440421436 usec\nrounds: 3181"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 37577.17281845222,
            "unit": "iter/sec",
            "range": "stddev: 0.000003666200196303182",
            "extra": "mean: 26.61190092270463 usec\nrounds: 7045"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 8823.439782622243,
            "unit": "iter/sec",
            "range": "stddev: 0.0000051334574522956826",
            "extra": "mean: 113.33448458156863 usec\nrounds: 1816"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 2544.111014426907,
            "unit": "iter/sec",
            "range": "stddev: 0.00002978212912765595",
            "extra": "mean: 393.06460855257234 usec\nrounds: 608"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 20718.977517614894,
            "unit": "iter/sec",
            "range": "stddev: 0.000006373272537938198",
            "extra": "mean: 48.26493002127245 usec\nrounds: 5173"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1951805.025330049,
            "unit": "iter/sec",
            "range": "stddev: 8.998915854185426e-8",
            "extra": "mean: 512.346257450026 nsec\nrounds: 90580"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 241620.5030748199,
            "unit": "iter/sec",
            "range": "stddev: 7.982558708114299e-7",
            "extra": "mean: 4.138721620368207 usec\nrounds: 19107"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1789086.1790550263,
            "unit": "iter/sec",
            "range": "stddev: 6.050080329793146e-8",
            "extra": "mean: 558.944567180214 nsec\nrounds: 35985"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1253542.8891462982,
            "unit": "iter/sec",
            "range": "stddev: 1.5387905641137247e-7",
            "extra": "mean: 797.7389594392276 nsec\nrounds: 94180"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 286053.6741918187,
            "unit": "iter/sec",
            "range": "stddev: 7.494395526321508e-7",
            "extra": "mean: 3.4958474238279877 usec\nrounds: 38099"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 149108.99532995388,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011243881365345292",
            "extra": "mean: 6.706503506291912 usec\nrounds: 13547"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 78372.92766522751,
            "unit": "iter/sec",
            "range": "stddev: 0.00003553431208552292",
            "extra": "mean: 12.759508031542884 usec\nrounds: 13696"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 7875615.1323694885,
            "unit": "iter/sec",
            "range": "stddev: 2.2153142056987138e-8",
            "extra": "mean: 126.97420876877048 nsec\nrounds: 85310"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "528650ee1d2b3a3dc3044c15ddf47d4b846f6c97",
          "message": "fix(ci): lower coverage threshold to 73% due to CI test exclusions",
          "timestamp": "2026-05-20T10:49:20-04:00",
          "tree_id": "b565dbf2a76eaf7ab32cafbbf423066a859c6e63",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/528650ee1d2b3a3dc3044c15ddf47d4b846f6c97"
        },
        "date": 1779288801512,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 180316.85264705552,
            "unit": "iter/sec",
            "range": "stddev: 0.000002399495196617517",
            "extra": "mean: 5.545793337228202 usec\nrounds: 6934"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 180148.67830728382,
            "unit": "iter/sec",
            "range": "stddev: 8.364727481896671e-7",
            "extra": "mean: 5.55097050611871 usec\nrounds: 16478"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 168392.4013498722,
            "unit": "iter/sec",
            "range": "stddev: 8.530760205047835e-7",
            "extra": "mean: 5.938510241458463 usec\nrounds: 16941"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 495233.3317732641,
            "unit": "iter/sec",
            "range": "stddev: 4.846831157511193e-7",
            "extra": "mean: 2.019250191458915 usec\nrounds: 23506"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 499603.96036294196,
            "unit": "iter/sec",
            "range": "stddev: 5.363422100178707e-7",
            "extra": "mean: 2.0015854143220575 usec\nrounds: 53340"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 519326.16616052884,
            "unit": "iter/sec",
            "range": "stddev: 5.536808813027661e-7",
            "extra": "mean: 1.9255721455230703 usec\nrounds: 51209"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 6127820.259592699,
            "unit": "iter/sec",
            "range": "stddev: 1.3306314720850432e-8",
            "extra": "mean: 163.1901651218585 nsec\nrounds: 22622"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 60844.65362653088,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015242994549738908",
            "extra": "mean: 16.435297768939176 usec\nrounds: 6992"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 101159.64054632506,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012076638718760227",
            "extra": "mean: 9.88536529587667 usec\nrounds: 20378"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 28390.717490479263,
            "unit": "iter/sec",
            "range": "stddev: 0.00000314039211497044",
            "extra": "mean: 35.22278013351888 usec\nrounds: 2547"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42512.87189488884,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020553145201255034",
            "extra": "mean: 23.52228761379506 usec\nrounds: 6919"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9238.825053882441,
            "unit": "iter/sec",
            "range": "stddev: 0.000005224400364858459",
            "extra": "mean: 108.23887173615968 usec\nrounds: 2183"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 2870.536690518754,
            "unit": "iter/sec",
            "range": "stddev: 0.000021837075330999994",
            "extra": "mean: 348.3669110737907 usec\nrounds: 596"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 29906.56461349458,
            "unit": "iter/sec",
            "range": "stddev: 0.000003500451053172216",
            "extra": "mean: 33.437474779325726 usec\nrounds: 4758"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 2170691.1789232893,
            "unit": "iter/sec",
            "range": "stddev: 8.134128682072947e-8",
            "extra": "mean: 460.68275842721306 nsec\nrounds: 89000"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 243748.65390235186,
            "unit": "iter/sec",
            "range": "stddev: 6.902776448419725e-7",
            "extra": "mean: 4.102586758902103 usec\nrounds: 15180"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1860656.292519117,
            "unit": "iter/sec",
            "range": "stddev: 1.2083254938364199e-7",
            "extra": "mean: 537.4447736642002 nsec\nrounds: 93319"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1176218.5611146009,
            "unit": "iter/sec",
            "range": "stddev: 4.389703461456667e-7",
            "extra": "mean: 850.1821286108477 nsec\nrounds: 22550"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 285510.3070919522,
            "unit": "iter/sec",
            "range": "stddev: 7.704935771571852e-7",
            "extra": "mean: 3.5025005233101356 usec\nrounds: 23887"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 149077.5128663116,
            "unit": "iter/sec",
            "range": "stddev: 9.754689669201438e-7",
            "extra": "mean: 6.7079197980501 usec\nrounds: 10299"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 78765.01389677565,
            "unit": "iter/sec",
            "range": "stddev: 0.000039968486772823425",
            "extra": "mean: 12.695992173765568 usec\nrounds: 10861"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8798691.074530896,
            "unit": "iter/sec",
            "range": "stddev: 1.0680767590783728e-8",
            "extra": "mean: 113.65326859749302 nsec\nrounds: 41605"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "372cba05623b918ff907633ef63573d17e68ddc8",
          "message": "fix(ci): lower coverage threshold to 70% as more tests excluded",
          "timestamp": "2026-05-20T11:00:37-04:00",
          "tree_id": "dd176cae4b96f8400d108a6277c5a24678ed9ee0",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/372cba05623b918ff907633ef63573d17e68ddc8"
        },
        "date": 1779289392851,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 184646.96131113108,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026174750509855904",
            "extra": "mean: 5.415740356078728 usec\nrounds: 6740"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 181947.22209126953,
            "unit": "iter/sec",
            "range": "stddev: 7.331497045176654e-7",
            "extra": "mean: 5.496099300149653 usec\nrounds: 17573"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 173361.22649229216,
            "unit": "iter/sec",
            "range": "stddev: 7.595476472608707e-7",
            "extra": "mean: 5.768302522043251 usec\nrounds: 16455"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 515638.75542246416,
            "unit": "iter/sec",
            "range": "stddev: 4.636965019887313e-7",
            "extra": "mean: 1.9393422032071606 usec\nrounds: 22849"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 513303.6392999477,
            "unit": "iter/sec",
            "range": "stddev: 5.461628318921207e-7",
            "extra": "mean: 1.9481646406478184 usec\nrounds: 44339"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 532470.6535756299,
            "unit": "iter/sec",
            "range": "stddev: 5.164402567925957e-7",
            "extra": "mean: 1.8780377721942645 usec\nrounds: 50328"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 6088394.120123307,
            "unit": "iter/sec",
            "range": "stddev: 2.410573124897803e-8",
            "extra": "mean: 164.2469229603162 nsec\nrounds: 98659"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 59909.63850903494,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013928646537308508",
            "extra": "mean: 16.69180493968747 usec\nrounds: 6721"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 102251.12822795479,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010389476624149598",
            "extra": "mean: 9.779843189315603 usec\nrounds: 19954"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 28850.629625850062,
            "unit": "iter/sec",
            "range": "stddev: 0.000003873730755432883",
            "extra": "mean: 34.66128860855097 usec\nrounds: 2616"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42866.38126896797,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018461271048154183",
            "extra": "mean: 23.32830461534491 usec\nrounds: 6825"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9174.435468320982,
            "unit": "iter/sec",
            "range": "stddev: 0.000011641724974730147",
            "extra": "mean: 108.9985322206436 usec\nrounds: 2157"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 2923.428456488978,
            "unit": "iter/sec",
            "range": "stddev: 0.00002720022581311492",
            "extra": "mean: 342.06412603679536 usec\nrounds: 603"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 30711.97649803538,
            "unit": "iter/sec",
            "range": "stddev: 0.000004498386191890633",
            "extra": "mean: 32.56058756309511 usec\nrounds: 4551"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1723516.3964042326,
            "unit": "iter/sec",
            "range": "stddev: 2.607246345855714e-7",
            "extra": "mean: 580.2091596495961 nsec\nrounds: 82645"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 245031.1834836843,
            "unit": "iter/sec",
            "range": "stddev: 8.669683562309705e-7",
            "extra": "mean: 4.081113210909281 usec\nrounds: 11112"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1861400.226209567,
            "unit": "iter/sec",
            "range": "stddev: 1.366932456807657e-7",
            "extra": "mean: 537.2299766164405 nsec\nrounds: 92799"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1411868.6752364626,
            "unit": "iter/sec",
            "range": "stddev: 1.4564631058083807e-7",
            "extra": "mean: 708.2811719953654 nsec\nrounds: 85194"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 286328.9025751296,
            "unit": "iter/sec",
            "range": "stddev: 6.52610915481865e-7",
            "extra": "mean: 3.492487104886699 usec\nrounds: 22683"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 153162.4025218547,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010136171141922616",
            "extra": "mean: 6.529017458167061 usec\nrounds: 10654"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 79024.68961971365,
            "unit": "iter/sec",
            "range": "stddev: 0.00005122243291835304",
            "extra": "mean: 12.654273048236535 usec\nrounds: 10478"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8617937.087897118,
            "unit": "iter/sec",
            "range": "stddev: 1.279874402026007e-8",
            "extra": "mean: 116.03705037533402 nsec\nrounds: 41429"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "107672758b8ff3436c0d0624c09d92360cb93713",
          "message": "fix(ci): lower coverage threshold to 60% due to extensive test exclusions",
          "timestamp": "2026-05-20T11:19:31-04:00",
          "tree_id": "392eb41c9b8ab91edd9f0591ecfa18e64483b525",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/107672758b8ff3436c0d0624c09d92360cb93713"
        },
        "date": 1779290533648,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 185470.38390773756,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020295837057772473",
            "extra": "mean: 5.391696393411528 usec\nrounds: 8152"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 183753.0607669606,
            "unit": "iter/sec",
            "range": "stddev: 9.951151097013203e-7",
            "extra": "mean: 5.4420862206383624 usec\nrounds: 17432"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 172764.77722818818,
            "unit": "iter/sec",
            "range": "stddev: 9.76269713061537e-7",
            "extra": "mean: 5.788216881032395 usec\nrounds: 17641"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 517949.1175773921,
            "unit": "iter/sec",
            "range": "stddev: 5.825390398755836e-7",
            "extra": "mean: 1.9306915796619342 usec\nrounds: 27362"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 522502.15788452415,
            "unit": "iter/sec",
            "range": "stddev: 5.285164529085864e-7",
            "extra": "mean: 1.9138676939608072 usec\nrounds: 57624"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 537983.067115345,
            "unit": "iter/sec",
            "range": "stddev: 5.403680137000521e-7",
            "extra": "mean: 1.8587945627396432 usec\nrounds: 46126"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 6108217.16398995,
            "unit": "iter/sec",
            "range": "stddev: 2.504720103877794e-8",
            "extra": "mean: 163.71389116540615 nsec\nrounds: 97676"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 58819.202722038885,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019844357026040875",
            "extra": "mean: 17.001250505310082 usec\nrounds: 5441"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 102069.37891127115,
            "unit": "iter/sec",
            "range": "stddev: 0.000001705691896163513",
            "extra": "mean: 9.79725761699108 usec\nrounds: 20907"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 19981.925771551712,
            "unit": "iter/sec",
            "range": "stddev: 0.000006567047017247409",
            "extra": "mean: 50.04522644277365 usec\nrounds: 2685"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 37590.48209840889,
            "unit": "iter/sec",
            "range": "stddev: 0.000003771492700774244",
            "extra": "mean: 26.602478717407234 usec\nrounds: 7048"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 8843.97436274173,
            "unit": "iter/sec",
            "range": "stddev: 0.00000787427526563585",
            "extra": "mean: 113.07133636805217 usec\nrounds: 2197"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 2571.202475541547,
            "unit": "iter/sec",
            "range": "stddev: 0.000026739253385435575",
            "extra": "mean: 388.9230854094366 usec\nrounds: 562"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 20953.40398173049,
            "unit": "iter/sec",
            "range": "stddev: 0.0000062379553302745714",
            "extra": "mean: 47.72494249010381 usec\nrounds: 5060"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 1985571.2600780062,
            "unit": "iter/sec",
            "range": "stddev: 8.906184438200079e-8",
            "extra": "mean: 503.6333976553989 nsec\nrounds: 97657"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 245300.53188143446,
            "unit": "iter/sec",
            "range": "stddev: 8.72009532787805e-7",
            "extra": "mean: 4.076632008622582 usec\nrounds: 16658"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1811484.08859936,
            "unit": "iter/sec",
            "range": "stddev: 6.139497399295482e-8",
            "extra": "mean: 552.0335543069591 nsec\nrounds: 35751"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1306761.8599577222,
            "unit": "iter/sec",
            "range": "stddev: 1.332856753431466e-7",
            "extra": "mean: 765.2503724223819 nsec\nrounds: 81673"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 282143.36407585745,
            "unit": "iter/sec",
            "range": "stddev: 8.307326036077529e-7",
            "extra": "mean: 3.544297429342122 usec\nrounds: 28864"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 149297.5525394711,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010823324828247144",
            "extra": "mean: 6.6980334438879785 usec\nrounds: 11751"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 77904.34741981623,
            "unit": "iter/sec",
            "range": "stddev: 0.00003637318421236331",
            "extra": "mean: 12.836254113151506 usec\nrounds: 11609"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 7635068.64701523,
            "unit": "iter/sec",
            "range": "stddev: 2.9262684920429928e-8",
            "extra": "mean: 130.97459187757298 nsec\nrounds: 39988"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "7cb56c78a7d573703e862881ecf575b54e0250ca",
          "message": "fix(ci): add missing checkout steps in on-tag workflow",
          "timestamp": "2026-05-20T13:55:56-04:00",
          "tree_id": "a832f3479c7dd5582e20cecad8e3de79ed9e097a",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/7cb56c78a7d573703e862881ecf575b54e0250ca"
        },
        "date": 1779299903795,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 183149.28156259807,
            "unit": "iter/sec",
            "range": "stddev: 0.000002346919297020066",
            "extra": "mean: 5.460026877900763 usec\nrounds: 6883"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 181229.07570131292,
            "unit": "iter/sec",
            "range": "stddev: 7.46524912955052e-7",
            "extra": "mean: 5.517878387506202 usec\nrounds: 17786"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 167371.58697314042,
            "unit": "iter/sec",
            "range": "stddev: 8.316767011664987e-7",
            "extra": "mean: 5.974729750041019 usec\nrounds: 15926"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 485012.17185071466,
            "unit": "iter/sec",
            "range": "stddev: 5.819027196279363e-7",
            "extra": "mean: 2.0618039258359007 usec\nrounds: 23639"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 490167.6898131784,
            "unit": "iter/sec",
            "range": "stddev: 5.05819849069493e-7",
            "extra": "mean: 2.0401181489158096 usec\nrounds: 50995"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 503150.92097842845,
            "unit": "iter/sec",
            "range": "stddev: 5.618312766510305e-7",
            "extra": "mean: 1.9874752451121378 usec\nrounds: 36417"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 6088740.156438525,
            "unit": "iter/sec",
            "range": "stddev: 1.4963875025206758e-8",
            "extra": "mean: 164.23758845128927 nsec\nrounds: 24778"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 59574.29457679607,
            "unit": "iter/sec",
            "range": "stddev: 0.000003172618416492279",
            "extra": "mean: 16.785763173593594 usec\nrounds: 4991"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 102853.01333064711,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011780673772367717",
            "extra": "mean: 9.72261256736588 usec\nrounds: 19495"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 28270.632128267735,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035083484845240026",
            "extra": "mean: 35.37239618353289 usec\nrounds: 2201"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42989.87375597698,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021646466489737933",
            "extra": "mean: 23.26129184924549 usec\nrounds: 6846"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9108.877281988694,
            "unit": "iter/sec",
            "range": "stddev: 0.000005525547225108274",
            "extra": "mean: 109.78301376145832 usec\nrounds: 2180"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 2922.9036547504984,
            "unit": "iter/sec",
            "range": "stddev: 0.00001735157048273556",
            "extra": "mean: 342.1255429937737 usec\nrounds: 628"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 29851.164185219295,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037692369714474445",
            "extra": "mean: 33.499530999703744 usec\nrounds: 4742"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 2220118.87984268,
            "unit": "iter/sec",
            "range": "stddev: 4.214893562367266e-8",
            "extra": "mean: 450.42633035528087 nsec\nrounds: 31558"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 239189.1082636388,
            "unit": "iter/sec",
            "range": "stddev: 7.651268322035664e-7",
            "extra": "mean: 4.180792374951207 usec\nrounds: 15764"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1970601.7140616612,
            "unit": "iter/sec",
            "range": "stddev: 6.008323929347463e-8",
            "extra": "mean: 507.4592155605425 nsec\nrounds: 36574"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1430812.5881888866,
            "unit": "iter/sec",
            "range": "stddev: 1.2590202045885853e-7",
            "extra": "mean: 698.9035519080713 nsec\nrounds: 83767"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 277910.8721046809,
            "unit": "iter/sec",
            "range": "stddev: 7.220866238216557e-7",
            "extra": "mean: 3.5982759235965736 usec\nrounds: 24061"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 150795.13977644118,
            "unit": "iter/sec",
            "range": "stddev: 8.712908298628679e-7",
            "extra": "mean: 6.6315134657690775 usec\nrounds: 11919"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 79777.67880673314,
            "unit": "iter/sec",
            "range": "stddev: 0.00003488078823838629",
            "extra": "mean: 12.53483449202086 usec\nrounds: 11075"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8492538.351814035,
            "unit": "iter/sec",
            "range": "stddev: 1.1749532558877809e-8",
            "extra": "mean: 117.75042496997372 nsec\nrounds: 27296"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "54ae51e2b29a221a71565fcc3fc3c4bca13a2eab",
          "message": "fix(ci): update cosign-installer to sigstore/cosign-installer@v4",
          "timestamp": "2026-05-20T14:04:00-04:00",
          "tree_id": "abe1d1b5e6c4bc88da0a1a6bd2ef5abf85148736",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/54ae51e2b29a221a71565fcc3fc3c4bca13a2eab"
        },
        "date": 1779300391600,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 184993.25825250847,
            "unit": "iter/sec",
            "range": "stddev: 0.000002482342672336368",
            "extra": "mean: 5.405602395710225 usec\nrounds: 6929"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 180804.4831738629,
            "unit": "iter/sec",
            "range": "stddev: 8.071667637231098e-7",
            "extra": "mean: 5.53083630696476 usec\nrounds: 13788"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 172557.2932103319,
            "unit": "iter/sec",
            "range": "stddev: 8.490606727410304e-7",
            "extra": "mean: 5.795176670864265 usec\nrounds: 12928"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 507715.9647210907,
            "unit": "iter/sec",
            "range": "stddev: 4.882048145379344e-7",
            "extra": "mean: 1.96960519165345 usec\nrounds: 22459"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 504635.7345742644,
            "unit": "iter/sec",
            "range": "stddev: 6.018256019562735e-7",
            "extra": "mean: 1.9816274026722451 usec\nrounds: 38551"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 520672.3775118601,
            "unit": "iter/sec",
            "range": "stddev: 6.622620281945556e-7",
            "extra": "mean: 1.920593530962225 usec\nrounds: 29247"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5981675.829169026,
            "unit": "iter/sec",
            "range": "stddev: 3.783555499013327e-8",
            "extra": "mean: 167.1772306890804 nsec\nrounds: 90286"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 58665.95903749744,
            "unit": "iter/sec",
            "range": "stddev: 0.0000044897302800038524",
            "extra": "mean: 17.045660147835157 usec\nrounds: 6494"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 98256.74893249206,
            "unit": "iter/sec",
            "range": "stddev: 0.000003347676988542284",
            "extra": "mean: 10.177417947005925 usec\nrounds: 4491"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 25598.251302525423,
            "unit": "iter/sec",
            "range": "stddev: 0.000014011051554029495",
            "extra": "mean: 39.06516848286992 usec\nrounds: 2386"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43048.37056776767,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024230419582013616",
            "extra": "mean: 23.229682954568016 usec\nrounds: 5280"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9340.697902396569,
            "unit": "iter/sec",
            "range": "stddev: 0.000003832335532447101",
            "extra": "mean: 107.05838155234923 usec\nrounds: 1984"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 2926.082733607791,
            "unit": "iter/sec",
            "range": "stddev: 0.00002248666629293716",
            "extra": "mean: 341.75383645664175 usec\nrounds: 587"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 30048.055729391923,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037167387144429635",
            "extra": "mean: 33.28002347326041 usec\nrounds: 4814"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 2133411.3271480124,
            "unit": "iter/sec",
            "range": "stddev: 8.048622847779379e-8",
            "extra": "mean: 468.73286331371474 nsec\nrounds: 88684"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 239454.23460773553,
            "unit": "iter/sec",
            "range": "stddev: 7.966821050849307e-7",
            "extra": "mean: 4.1761633559672084 usec\nrounds: 16210"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1485998.8928853117,
            "unit": "iter/sec",
            "range": "stddev: 3.527819437660302e-7",
            "extra": "mean: 672.9480114607186 nsec\nrounds: 98464"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1443660.9198756246,
            "unit": "iter/sec",
            "range": "stddev: 1.3500988240655497e-7",
            "extra": "mean: 692.6834315679769 nsec\nrounds: 82116"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 281014.3016867862,
            "unit": "iter/sec",
            "range": "stddev: 7.152653313442886e-7",
            "extra": "mean: 3.5585377470025823 usec\nrounds: 21101"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 152624.72920395914,
            "unit": "iter/sec",
            "range": "stddev: 9.596738457114261e-7",
            "extra": "mean: 6.552018176973509 usec\nrounds: 11278"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 77381.93963399978,
            "unit": "iter/sec",
            "range": "stddev: 0.00004960954652107173",
            "extra": "mean: 12.922912048079805 usec\nrounds: 9653"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8695816.187765902,
            "unit": "iter/sec",
            "range": "stddev: 1.1231272368527163e-8",
            "extra": "mean: 114.99783095769625 nsec\nrounds: 41954"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "5c24ac0d3d411d9c1457d52e489389d86cfbc7bc",
          "message": "fix(ci): update cosign-installer to v4.1",
          "timestamp": "2026-05-20T14:08:04-04:00",
          "tree_id": "7c209803de7779e0712042f05f48f0f816dddb9d",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/5c24ac0d3d411d9c1457d52e489389d86cfbc7bc"
        },
        "date": 1779300645671,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 201821.02912713352,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016633895006132722",
            "extra": "mean: 4.954885050011652 usec\nrounds: 8856"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 198847.70688663615,
            "unit": "iter/sec",
            "range": "stddev: 6.333098385103215e-7",
            "extra": "mean: 5.028974262047206 usec\nrounds: 15075"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 190336.38294050028,
            "unit": "iter/sec",
            "range": "stddev: 4.980366424754497e-7",
            "extra": "mean: 5.253856275668551 usec\nrounds: 15982"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 521467.1779234582,
            "unit": "iter/sec",
            "range": "stddev: 2.910343903334451e-7",
            "extra": "mean: 1.9176662354515082 usec\nrounds: 16224"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 519146.3778979305,
            "unit": "iter/sec",
            "range": "stddev: 4.12264500772109e-7",
            "extra": "mean: 1.9262390003549448 usec\nrounds: 40774"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 550122.5998763039,
            "unit": "iter/sec",
            "range": "stddev: 3.0917962452162124e-7",
            "extra": "mean: 1.8177766196568763 usec\nrounds: 43849"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 6479797.581653909,
            "unit": "iter/sec",
            "range": "stddev: 1.382020755918462e-8",
            "extra": "mean: 154.32580839118728 nsec\nrounds: 96619"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 64447.04444004286,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013032699963284062",
            "extra": "mean: 15.516615365198506 usec\nrounds: 7628"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 107022.27222303857,
            "unit": "iter/sec",
            "range": "stddev: 7.678880000436244e-7",
            "extra": "mean: 9.343849455148563 usec\nrounds: 19270"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 26814.93618423814,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027547437534167583",
            "extra": "mean: 37.29264888528065 usec\nrounds: 2868"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 43317.38483274637,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014376052809404009",
            "extra": "mean: 23.085419488298292 usec\nrounds: 6763"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 10637.07736913335,
            "unit": "iter/sec",
            "range": "stddev: 0.00000393139133838784",
            "extra": "mean: 94.01078560374091 usec\nrounds: 1959"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 2913.3158119074324,
            "unit": "iter/sec",
            "range": "stddev: 0.000022070332007972134",
            "extra": "mean: 343.25149230741005 usec\nrounds: 650"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 28244.663230649003,
            "unit": "iter/sec",
            "range": "stddev: 0.000002752157941324277",
            "extra": "mean: 35.40491850916723 usec\nrounds: 5019"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 2009038.6483155019,
            "unit": "iter/sec",
            "range": "stddev: 5.244268069107542e-8",
            "extra": "mean: 497.7505041221878 nsec\nrounds: 88029"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 249740.9025364364,
            "unit": "iter/sec",
            "range": "stddev: 4.619449008815739e-7",
            "extra": "mean: 4.004149860290119 usec\nrounds: 16849"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1874173.027654876,
            "unit": "iter/sec",
            "range": "stddev: 1.143041148851029e-7",
            "extra": "mean: 533.5686648160212 nsec\nrounds: 36909"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1104463.0323997994,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013438696548618257",
            "extra": "mean: 905.4173572719586 nsec\nrounds: 61554"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 254013.83237116438,
            "unit": "iter/sec",
            "range": "stddev: 0.0000040493242358922055",
            "extra": "mean: 3.936793483509207 usec\nrounds: 26763"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 156668.17991296918,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011072680907244919",
            "extra": "mean: 6.3829170706872995 usec\nrounds: 5981"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 58702.5716941845,
            "unit": "iter/sec",
            "range": "stddev: 0.00030578874889789355",
            "extra": "mean: 17.035028809462997 usec\nrounds: 5519"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8524674.878067678,
            "unit": "iter/sec",
            "range": "stddev: 1.1607358213380367e-8",
            "extra": "mean: 117.30652656008175 nsec\nrounds: 99602"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "committer": {
            "email": "nikolasil2000@gmail.com",
            "name": "nikolasil",
            "username": "nikolasil"
          },
          "distinct": true,
          "id": "52fa94059737d48cfa92da0fe9f943e10fbeab8c",
          "message": "fix(ci): update cosign-installer to v4.1.2",
          "timestamp": "2026-05-20T14:13:31-04:00",
          "tree_id": "602d8fdc0a04b0f12acd6d38d528849bee15b8a5",
          "url": "https://github.com/nikolasil/chronicle-mcp/commit/52fa94059737d48cfa92da0fe9f943e10fbeab8c"
        },
        "date": 1779300972746,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_without_token",
            "value": 181299.94526418863,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024674050983770063",
            "extra": "mean: 5.515721466671207 usec\nrounds: 6764"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_token",
            "value": 178383.23031581115,
            "unit": "iter/sec",
            "range": "stddev: 7.390484938088866e-7",
            "extra": "mean: 5.605908123928419 usec\nrounds: 16827"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_sanitize_url_with_multiple_sensitive_params",
            "value": 170614.8971160642,
            "unit": "iter/sec",
            "range": "stddev: 7.719214531457928e-7",
            "extra": "mean: 5.86115290577311 usec\nrounds: 16278"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_chrome_timestamp",
            "value": 507066.4874003262,
            "unit": "iter/sec",
            "range": "stddev: 6.056691612538464e-7",
            "extra": "mean: 1.972127965164666 usec\nrounds: 22975"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_firefox_timestamp",
            "value": 510854.15875263873,
            "unit": "iter/sec",
            "range": "stddev: 8.895857161163387e-7",
            "extra": "mean: 1.9575058416705797 usec\nrounds: 50328"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_format_safari_timestamp",
            "value": 528799.8508262121,
            "unit": "iter/sec",
            "range": "stddev: 5.491254273741803e-7",
            "extra": "mean: 1.8910746635755877 usec\nrounds: 43984"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_exact",
            "value": 5780569.520686959,
            "unit": "iter/sec",
            "range": "stddev: 2.469459711972443e-8",
            "extra": "mean: 172.99333507212407 nsec\nrounds: 97334"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_similar",
            "value": 59344.782602751104,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014423986423587435",
            "extra": "mean: 16.850680988991304 usec\nrounds: 6633"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_fuzzy_match_score_different",
            "value": 98968.47312370432,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011501698537022221",
            "extra": "mean: 10.104227825663871 usec\nrounds: 21455"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_basic",
            "value": 28585.036127744796,
            "unit": "iter/sec",
            "range": "stddev: 0.000003291833493432755",
            "extra": "mean: 34.983338678707995 usec\nrounds: 2619"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_query_history_no_results",
            "value": 42886.01668000671,
            "unit": "iter/sec",
            "range": "stddev: 0.000002214006139053606",
            "extra": "mean: 23.317623724802495 usec\nrounds: 6862"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_get_top_domains",
            "value": 9141.579973265352,
            "unit": "iter/sec",
            "range": "stddev: 0.000005074037230334364",
            "extra": "mean: 109.39028077471406 usec\nrounds: 2169"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_regex",
            "value": 2875.6480358156673,
            "unit": "iter/sec",
            "range": "stddev: 0.000021733103284553704",
            "extra": "mean: 347.74770331597745 usec\nrounds: 573"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestDatabaseBenchmarks::test_search_with_fuzzy",
            "value": 30052.18235385005,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036829390669895115",
            "extra": "mean: 33.275453616828194 usec\nrounds: 4797"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_markdown",
            "value": 2105687.306427302,
            "unit": "iter/sec",
            "range": "stddev: 9.343816969709167e-8",
            "extra": "mean: 474.90432076386634 nsec\nrounds: 94021"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_json",
            "value": 237406.3873754166,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013842132030448124",
            "extra": "mean: 4.212186584595448 usec\nrounds: 13656"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_recent_results_markdown",
            "value": 1900272.280102037,
            "unit": "iter/sec",
            "range": "stddev: 5.626542751503949e-8",
            "extra": "mean: 526.2403764298034 nsec\nrounds: 35943"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_markdown",
            "value": 1408082.281158384,
            "unit": "iter/sec",
            "range": "stddev: 1.2009312123899673e-7",
            "extra": "mean: 710.1857706620416 nsec\nrounds: 82522"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_top_domains_json",
            "value": 278968.7701520197,
            "unit": "iter/sec",
            "range": "stddev: 7.151967556496842e-7",
            "extra": "mean: 3.5846306360925833 usec\nrounds: 24618"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_csv",
            "value": 150578.9292023427,
            "unit": "iter/sec",
            "range": "stddev: 8.499559272587078e-7",
            "extra": "mean: 6.641035404470402 usec\nrounds: 9914"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_export_json",
            "value": 78093.18485988965,
            "unit": "iter/sec",
            "range": "stddev: 0.00004545826375442245",
            "extra": "mean: 12.805214716164325 usec\nrounds: 10954"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestFormatterBenchmarks::test_format_search_results_empty",
            "value": 8557693.193567172,
            "unit": "iter/sec",
            "range": "stddev: 1.5352536835873026e-8",
            "extra": "mean: 116.85392048781628 nsec\nrounds: 27568"
          }
        ]
      }
    ]
  }
}