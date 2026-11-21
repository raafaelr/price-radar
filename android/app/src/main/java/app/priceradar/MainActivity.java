package app.priceradar;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceRequest;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.JSONObject;

public class MainActivity extends Activity {
    // Pagina embutida no APK; ela le os precos direto do repo (raw.githubusercontent.com)
    private static final String HOME = "file:///android_asset/index.html";
    private WebView web;

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        web = new WebView(this);
        web.getSettings().setJavaScriptEnabled(true);
        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r) {
                if (r.getUrl().toString().startsWith(HOME)) return false;
                startActivity(new Intent(Intent.ACTION_VIEW, r.getUrl())); // lojas abrem no navegador
                return true;
            }
        });
        web.addJavascriptInterface(new Object() {
            // Busca a URL pelo celular (sem CORS) e devolve para a pagina em window.__net(id, status, corpo)
            @JavascriptInterface
            public void get(final String id, final String url) {
                new Thread(() -> {
                    int code = 0; String body = "";
                    try {
                        HttpURLConnection c = (HttpURLConnection) new URL(url).openConnection();
                        c.setConnectTimeout(15000); c.setReadTimeout(20000);
                        c.setRequestProperty("User-Agent", "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/124 Mobile Safari/537.36");
                        c.setRequestProperty("Accept-Language", "pt-BR,pt;q=0.9");
                        code = c.getResponseCode();
                        InputStream in = code < 400 ? c.getInputStream() : c.getErrorStream();
                        ByteArrayOutputStream o = new ByteArrayOutputStream();
                        byte[] buf = new byte[16384]; int n;
                        while (in != null && (n = in.read(buf)) > 0) o.write(buf, 0, n);
                        body = o.toString("UTF-8");
                    } catch (Exception e) { code = -1; }
                    final String js = "window.__net(" + JSONObject.quote(id) + "," + code + "," + JSONObject.quote(body) + ")";
                    runOnUiThread(() -> web.evaluateJavascript(js, null));
                }).start();
            }
        }, "Net");
        setContentView(web);
        web.loadUrl(HOME);
    }

    @Override
    public void onBackPressed() {
        if (web.canGoBack()) web.goBack(); else super.onBackPressed();
    }
}
